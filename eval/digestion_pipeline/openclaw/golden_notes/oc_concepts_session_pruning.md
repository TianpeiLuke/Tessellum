---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - session_pruning
keywords:
  - openclaw session pruning
  - prune old tool results
  - anthropic prompt cache optimization
  - soft-trim hard-clear tool results
  - cache-ttl context pruning
  - legacy image cleanup replay view
  - contextPruning mode ttl
  - pruning vs compaction
topics:
  - OpenClaw
  - Session Pruning
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/session-pruning
access_control_group: ["general"]
---

# OpenClaw — Session Pruning

## Overview

This note defines OpenClaw **session pruning**: the in-memory trimming of **old tool results** from the context before each LLM call, which reduces context bloat from accumulated tool outputs (exec results, file reads, search results) without rewriting normal conversation text. Pruning is in-memory only — it does NOT modify the on-disk session transcript, so the full history is always preserved. This note mirrors the `concepts/session-pruning` source page: why pruning matters (Anthropic prompt-cache cost), the five-step cache-TTL mechanism, the separate legacy-image-cleanup replay view, the Anthropic smart defaults, how to enable or disable it via `contextPruning`, and the contrast with compaction.

## Why It Matters

Long sessions accumulate tool output that inflates the context window. This increases cost and can force [compaction](https://docs.openclaw.ai/concepts/compaction) sooner than necessary. Pruning is especially valuable for **Anthropic prompt caching**: after the cache TTL expires, the next request re-caches the full prompt, so pruning reduces the cache-write size and directly lowers cost.

## How It Works

Normal cache-TTL pruning runs as a five-step sequence before an LLM request:

1. Wait for the cache TTL to expire (default 5 minutes).
2. Find old tool results for normal pruning (conversation text is left alone).
3. **Soft-trim** oversized results — keep the head and tail, insert `...`.
4. **Hard-clear** the rest — replace with a placeholder.
5. Reset the TTL so follow-up requests reuse the fresh cache.

## Legacy Image Cleanup

OpenClaw also builds a separate idempotent **replay view** for sessions that persist raw image blocks or prompt-hydration media markers in history. It preserves the **3 most recent completed turns** byte-for-byte so prompt cache prefixes for recent follow-ups stay stable. In the replay view, older already-processed image blocks from `user` or `toolResult` history can be replaced with `[image data removed - already processed by model]`. Older textual media references such as `[media attached: ...]`, `[Image: source: ...]`, and `media://inbound/...` can be replaced with `[media reference removed - already processed by model]`; current-turn attachment markers stay intact so vision models can still hydrate fresh images. The raw session transcript is not rewritten, so history viewers can still render the original message entries and their images. This is separate from normal cache-TTL pruning — it exists to stop repeated image payloads or stale media refs from busting prompt caches on later turns.

## Smart Defaults

OpenClaw auto-enables pruning for Anthropic profiles. If you set explicit values, OpenClaw does not override them.

| Profile type                                            | Pruning enabled | Heartbeat |
| ------------------------------------------------------- | --------------- | --------- |
| Anthropic OAuth/token auth (including Claude CLI reuse) | Yes             | 1 hour    |
| API key                                                 | Yes             | 30 min    |

## Enable or Disable

Pruning is off by default for non-Anthropic providers. To enable, set the `contextPruning` block under `agents.defaults`:

```json5
{
  agents: {
    defaults: {
      contextPruning: { mode: "cache-ttl", ttl: "5m" },
    },
  },
}
```

To disable: set `mode: "off"`.

## Pruning vs Compaction

Pruning and compaction are complementary context-reduction mechanisms — pruning keeps tool output lean between compaction cycles.

|            | Pruning            | Compaction              |
| ---------- | ------------------ | ----------------------- |
| **What**   | Trims tool results | Summarizes conversation |
| **Saved?** | No (per-request)   | Yes (in transcript)     |
| **Scope**  | Tool results only  | Entire conversation     |

**Source**: OpenClaw documentation — `concepts/session-pruning` (mirror `inbox/openclaw_docs/concepts/session-pruning.md`)
**Last Updated**: 2026-06-22
**Status**: Active
