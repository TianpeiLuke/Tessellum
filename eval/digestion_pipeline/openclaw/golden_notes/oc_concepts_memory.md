---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - memory
keywords:
  - openclaw memory model
  - memory.md daily notes dreams.md
  - action-sensitive memories
  - inferred commitments
  - memory_search memory_get
  - automatic memory flush
  - dreaming grounded backfill
  - memory backends builtin qmd honcho lancedb
topics:
  - OpenClaw
  - Memory
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/memory
access_control_group: ["general"]
---

# OpenClaw — The Memory Model

## Overview

This note captures the OpenClaw **memory model**: how an agent remembers across sessions by writing **plain Markdown files** in its workspace, with no hidden state — the model only "remembers" what gets saved to disk. It mirrors the `concepts/memory` source page in full, covering the three memory files (`MEMORY.md`, daily `memory/YYYY-MM-DD.md` notes, optional `DREAMS.md`), the what-goes-where layering and bootstrap-budget truncation, action-sensitive memories and inferred commitments, the `memory_search` / `memory_get` tools and the `memory-wiki` companion, hybrid memory search, the four memory backends, the automatic pre-compaction memory flush, dreaming, grounded backfill and live promotion, and the `openclaw memory` CLI. Detail-only topics (dreaming internals, the search pipeline, the QMD/LanceDB backends, commitments, compaction, the config reference) are LINKED out, not duplicated here.

## How It Works

An OpenClaw agent has three memory-related files that live in the agent workspace (default `~/.openclaw/workspace`):

- **`MEMORY.md`** — long-term memory: durable facts, preferences, and decisions. It is loaded at the start of every DM session.
- **`memory/YYYY-MM-DD.md`** (or **`memory/YYYY-MM-DD-<slug>.md`**) — daily notes holding running context and observations. Today and yesterday's notes are loaded automatically, and slugged variants — such as those written by the bundled session-memory hook on `/new` or `/reset` — are now picked up alongside the date-only file.
- **`DREAMS.md`** (optional) — the Dream Diary and dreaming-sweep summaries for human review, including grounded historical backfill entries.

## What Goes Where

`MEMORY.md` is the compact, curated layer. Use it for durable facts, preferences, standing decisions, and short summaries that should be available at the start of a main private session; it is not meant to be a raw transcript, daily log, or exhaustive archive. The `memory/YYYY-MM-DD.md` files are the working layer: detailed daily notes, observations, session summaries, and raw context that may still be useful later. These daily files are indexed for `memory_search` and `memory_get`, but they are NOT injected into the normal bootstrap prompt on every turn.

Over time, the agent is expected to distill useful material from daily notes into `MEMORY.md` and remove stale long-term entries — the generated workspace instructions and heartbeat flow can do that periodically, so you do not need to manually edit `MEMORY.md` for every remembered detail. If `MEMORY.md` grows past the bootstrap file budget, OpenClaw keeps the on-disk file intact but truncates the copy injected into the model context; treat that as a signal to move detailed material back into `memory/*.md`, keep only the durable summary in `MEMORY.md`, or raise the bootstrap limits if you explicitly want to spend more prompt budget. Use `/context list`, `/context detail`, or `openclaw doctor` to see raw-vs-injected sizes and truncation status. To make the agent remember something, you can simply ask it (e.g. "Remember that I prefer TypeScript") and it will write the fact to the appropriate file.

## Action-Sensitive Memories

Most memories can be written as ordinary Markdown notes, but some memories affect what the agent should do later — for those, capture *when it is safe to act* on the note, not just the fact itself. Capture that action boundary when a note involves: approval or permission requirements; temporary constraints; handoffs to another session, thread, or person; expiry conditions; safe-to-act timing; source or owner authority; or instructions to avoid a tempting action.

A useful action-sensitive memory makes clear what changes future behavior, when or under what condition it applies, when it expires or what unlocks action, what the agent should avoid doing, and who is the source or owner if that affects trust or authority. Memory can preserve approval context, but it does NOT enforce policy — use OpenClaw approval settings, sandboxing, and scheduled tasks for hard operational controls. Two source examples illustrate the pattern:

```md
The API migration is being designed in another session. Future turns should not edit the API implementation from this thread; use findings here only as design input until the migration plan lands.
```

```md
A report from an untrusted source needs review before promotion. Future turns should treat it as evidence only; do not store it as durable memory until a trusted reviewer confirms the contents.
```

Use commitments for inferred, short-lived follow-ups, and scheduled tasks for exact reminders, timed checks, and recurring work; memory can still summarize the durable context around either path. This is not a required schema for every memory — simple facts can stay concise. Use action-sensitive boundaries when losing timing, authority, expiry, or safe-to-act context could cause the agent to do the wrong thing later.

## Inferred Commitments

Some future follow-ups are not durable facts: if you mention an interview tomorrow, the useful memory may be "check in after the interview," not "store this forever in `MEMORY.md`." Commitments are opt-in, short-lived follow-up memories for that case — OpenClaw infers them in a hidden background pass, scopes them to the same agent and channel, and delivers due check-ins through heartbeat. Explicit reminders still use scheduled tasks.

## Memory Tools

The agent has two tools for working with memory:

- **`memory_search`** — finds relevant notes using semantic search, even when the wording differs from the original.
- **`memory_get`** — reads a specific memory file or line range.

Both tools are provided by the active memory plugin (default: `memory-core`).

## Memory Wiki Companion Plugin

If you want durable memory to behave more like a maintained knowledge base than just raw notes, use the bundled `memory-wiki` plugin. `memory-wiki` compiles durable knowledge into a wiki vault with deterministic page structure, structured claims and evidence, contradiction and freshness tracking, generated dashboards, compiled digests for agent/runtime consumers, and wiki-native tools like `wiki_search`, `wiki_get`, `wiki_apply`, and `wiki_lint`. It does NOT replace the active memory plugin — the active memory plugin still owns recall, promotion, and dreaming, while `memory-wiki` adds a provenance-rich knowledge layer beside it.

## Memory Search

When an embedding provider is configured, `memory_search` uses **hybrid search** — combining vector similarity (semantic meaning) with keyword matching (exact terms like IDs and code symbols). This works out of the box once you have an API key for any supported provider. OpenClaw uses OpenAI embeddings by default; set `agents.defaults.memorySearch.provider` explicitly to use Gemini, Voyage, Mistral, local, Ollama, Bedrock, GitHub Copilot, or OpenAI-compatible embeddings. For how search works, tuning options, and provider setup, see the Memory Search page (linked under References).

## Memory Backends

OpenClaw supports four memory backends:

- **Builtin (default)** — SQLite-based; works out of the box with keyword search, vector similarity, and hybrid search, with no extra dependencies.
- **QMD** — a local-first sidecar with reranking, query expansion, and the ability to index directories outside the workspace.
- **Honcho** — AI-native cross-session memory with user modeling, semantic search, and multi-agent awareness; installed as a plugin.
- **LanceDB** — bundled LanceDB-backed memory with OpenAI-compatible embeddings, auto-recall, auto-capture, and local Ollama embedding support.

## Knowledge Wiki Layer

Alongside the backends, the **Memory Wiki** plugin compiles durable memory into a provenance-rich wiki vault with claims, dashboards, bridge mode, and Obsidian-friendly workflows (the companion described in "Memory Wiki Companion Plugin" above).

## Automatic Memory Flush

Before compaction summarizes your conversation, OpenClaw runs a silent turn that reminds the agent to save important context to memory files. This is on by default — you do not need to configure anything. To keep that housekeeping turn on a local model, set an exact memory-flush model override:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "model": "ollama/qwen3:8b"
        }
      }
    }
  }
}
```

The override applies ONLY to the memory-flush turn and does not inherit the active session fallback chain. The flush prevents context loss during compaction: if the agent has important facts in the conversation that are not yet written to a file, they are saved automatically before the summary happens.

## Dreaming

Dreaming is an optional background consolidation pass for memory. It collects short-term signals, scores candidates, and promotes only qualified items into long-term memory (`MEMORY.md`). It is designed to keep long-term memory high-signal and is **opt-in** (disabled by default); when enabled, `memory-core` auto-manages one recurring cron job for a full dreaming sweep. Promotions are **thresholded** — they must pass score, recall-frequency, and query-diversity gates — and **reviewable**: phase summaries and diary entries are written to `DREAMS.md` for human review. For phase behavior, scoring signals, and Dream Diary details, see the Dreaming page (linked under References).

## Grounded Backfill and Live Promotion

The dreaming system has two closely related review lanes. **Live dreaming** works from the short-term dreaming store under `memory/.dreams/` and is what the normal deep phase uses when deciding what can graduate into `MEMORY.md`. **Grounded backfill** reads historical `memory/YYYY-MM-DD.md` notes as standalone day files and writes structured review output into `DREAMS.md`; it is useful when you want to replay older notes and inspect what the system thinks is durable without manually editing `MEMORY.md`.

When you run:

```bash
openclaw memory rem-backfill --path ./memory --stage-short-term
```

the grounded durable candidates are NOT promoted directly — they are staged into the same short-term dreaming store the normal deep phase already uses. That means `DREAMS.md` stays the human review surface, the short-term store stays the machine-facing ranking surface, and `MEMORY.md` is still only written by deep promotion. If you decide the replay was not useful, you can remove the staged artifacts without touching ordinary diary entries or normal recall state:

```bash
openclaw memory rem-backfill --rollback
openclaw memory rem-backfill --rollback-short-term
```

## CLI

The core `openclaw memory` command surface:

```bash
openclaw memory status          # Check index status and provider
openclaw memory search "query"  # Search from the command line
openclaw memory index --force   # Rebuild the index
```

**Source**: OpenClaw documentation — `concepts/memory` (mirror `inbox/openclaw_docs/concepts/memory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
