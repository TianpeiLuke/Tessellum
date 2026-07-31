---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - context
keywords:
  - openclaw context
  - what counts toward context window
  - context list detail map
  - project context injected workspace files
  - bootstrapMaxChars bootstrapTotalMaxChars
  - tool schemas two costs
  - system prompt build
  - context vs memory
topics:
  - OpenClaw
  - Context
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/context
access_control_group: ["general"]
---

# OpenClaw — Context: What the Model Sees

## Overview

This note defines the OpenClaw **context** concept: "everything OpenClaw sends to the model for a run," bounded by the model's **context window** (token limit). It mirrors the `concepts/context` source page — distinguishing context from memory, enumerating what counts toward the window, how the OpenClaw-owned system prompt is rebuilt each run, how workspace **Project Context** files are injected and truncated, the two distinct costs tools impose, how slash commands/directives are handled before the model sees a message, what persists across messages (normal history vs compaction vs pruning), and how to inspect all of it via `/status`, `/context list|detail|map`, and `/usage tokens`. Mechanics of compaction, the system-prompt breakdown, the pluggable context engine, and slash-command behavior are LINKED to their home docs, not re-explained here.

## Context vs memory

In OpenClaw, **context is everything OpenClaw sends to the model for a run**, bounded by the model's **context window** (its token limit). The beginner mental model splits context into three parts: the OpenClaw-built **system prompt** (rules, tools, skills list, time/runtime metadata, and injected workspace files); the **conversation history** (your messages plus the assistant's messages for this session); and **tool calls/results plus attachments** (command output, file reads, images/audio, etc.). Context is *not the same thing* as "memory" — memory can be stored on disk and reloaded later, whereas context is what is inside the model's current window for the run in progress.

## Quick start (inspect context)

OpenClaw exposes several commands to inspect and reduce what is in the window. `/status` gives a quick "how full is my window?" view plus session settings. `/context list` shows what is injected plus rough sizes (per file plus totals). `/context detail` is a deeper breakdown — per-file, per-tool schema sizes, per-skill entry sizes, system-prompt size, and compactable transcript message counts. `/context map` returns a WinDirStat-style treemap image of the current session's tracked context contributors. `/usage tokens` appends a per-reply usage footer to normal replies. `/compact` summarizes older history into a compact entry to free window space. The page cross-references Slash commands, Token use & costs, and Compaction for the full behavior of these surfaces.

## Example output

The page shows illustrative output whose values "vary by model, provider, tool policy, and what's in your workspace." The `/context list` view reports the workspace dir, `Bootstrap max/file: 12,000 chars`, sandbox state, the run system-prompt size (`38,412 chars (~9,603 tok)` with a `Project Context 23,901 chars (~5,976 tok)` portion), and the per-file status of injected workspace files (e.g. `AGENTS.md: OK`, `TOOLS.md: TRUNCATED | raw 54,210 chars … | injected 20,962 chars …`, `HEARTBEAT.md: MISSING`). It then reports the skills-list system-prompt text size (`2,184 chars (~546 tok) (12 skills)`), the tool list, the tool-list system-prompt text size, the **tool schemas (JSON)** size (`31,988 chars (~7,997 tok) (counts toward context; not shown as text)`), and `Session tokens (cached): 14,250 total / ctx=32,000`. The `/context detail` view additionally surfaces a "Top skills (prompt entry size)" list and a "Top tools (schema size)" list (e.g. `browser: 9,812 chars (~2,453 tok)`).

The `/context map` view "sends an image generated from the latest cached run report." Before a normal message has produced a run report in the session, `/context map` returns an unavailable message instead of rendering an estimate; rectangle area is proportional to tracked prompt characters across injected workspace files, base system-prompt text, skill prompt entries, and tool JSON schemas. The `/context list`, `/context detail`, and `/context json` views can still inspect an on-demand estimate when no run report is cached.

## What counts toward the context window

Everything the model receives counts toward the window, including: the **system prompt** (all sections); the **conversation history**; **tool calls plus tool results**; **attachments/transcripts** (images/audio/files); **compaction summaries and pruning artifacts**; and provider "wrappers" or hidden headers (not visible, still counted). This is the accounting basis for the inspection commands — every contributor above shows up in the `/context` breakdown.

## How OpenClaw builds the system prompt

The system prompt is **OpenClaw-owned** and rebuilt each run. It includes the tool list plus short descriptions; the skills list (metadata only); the workspace location; the time (UTC plus converted user time if configured); runtime metadata (host/OS/model/thinking); and injected workspace bootstrap files under **Project Context**. The page defers the full section-by-section breakdown to the System Prompt doc.

## Injected workspace files (Project Context)

By default, OpenClaw injects a fixed set of workspace files (if present): `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, and `BOOTSTRAP.md` (first-run only). These appear in the system prompt under the **Project Context** label. Large files are truncated per-file using `agents.defaults.bootstrapMaxChars` (default `20000` chars), and OpenClaw also enforces a **total** bootstrap-injection cap across files via `agents.defaults.bootstrapTotalMaxChars` (default `60000` chars). `/context` shows **raw vs injected** sizes and whether truncation happened.

When truncation occurs, the runtime can inject an in-prompt warning block under Project Context. This is configured with `agents.defaults.bootstrapPromptTruncationWarning`, which accepts `off`, `once`, or `always` (default `always`).

## Skills: injected vs loaded on-demand

The system prompt includes a compact **skills list** (name plus description plus location), and "this list has real overhead." Skill instructions themselves are *not* included by default — the model is expected to `read` a skill's `SKILL.md` only when needed. This split keeps the always-present per-skill cost to the metadata entry while deferring the full instruction text to an on-demand file read.

## Tools: there are two costs

Tools affect context in two distinct ways. First, the **tool list text** appears in the system prompt (shown as "Tooling"). Second, the **tool schemas** (JSON) are sent to the model so it can call tools — these "count toward context even though you don't see them as plain text." `/context detail` breaks down the biggest tool schemas so you can see what dominates the budget.

## Commands, directives, and inline shortcuts

Slash commands are handled by the **Gateway**, with a few different behaviors. **Standalone commands** are messages that are only `/...` and run as a command. **Directives** — `/think`, `/verbose`, `/trace`, `/reasoning`, `/elevated`, `/model`, `/queue` — are stripped before the model sees the message; directive-only messages persist session settings, while inline directives in a normal message act as per-message hints. **Inline shortcuts** (allowlisted senders only) let certain `/...` tokens inside a normal message run immediately (example: "hey /status") and are stripped before the model sees the remaining text. The page defers the full command details to Slash commands.

## Sessions, compaction, and pruning (what persists)

What persists across messages depends on the mechanism. **Normal history** persists in the session transcript until compacted or pruned by policy. **Compaction** persists a summary into the transcript and keeps recent messages intact. **Pruning** drops old tool results from the *in-memory* prompt to free context-window space, but does not rewrite the session transcript — the full history is still inspectable on disk. The page cross-references Session, Compaction, and Session pruning for each mechanism.

By default, OpenClaw uses the built-in `legacy` context engine for assembly and compaction. If you install a plugin that provides `kind: "context-engine"` and select it with `plugins.slots.contextEngine`, OpenClaw delegates context assembly, `/compact`, and related subagent context lifecycle hooks to that engine instead. The page notes that `ownsCompaction: false` does not auto-fallback to the legacy engine — the active engine must still implement `compact()` correctly — and defers the full pluggable interface, lifecycle hooks, and configuration to the Context Engine doc.

## What `/context` actually reports

`/context` prefers the latest **run-built** system-prompt report when available. `System prompt (run)` is captured from the last embedded (tool-capable) run and persisted in the session store; `System prompt (estimate)` is computed on the fly when no run report exists (or when running via a CLI backend that does not generate the report). Either way it reports sizes and top contributors — it does **not** dump the full system prompt or tool schemas. In detailed mode it also compares the session transcript with the same real-conversation message predicate used by compaction, so high prompt/cache usage is easier to distinguish from compactable conversation history.

**Source**: OpenClaw documentation — `concepts/context` (mirror `inbox/openclaw_docs/concepts/context.md`)
**Last Updated**: 2026-06-22
**Status**: Active
