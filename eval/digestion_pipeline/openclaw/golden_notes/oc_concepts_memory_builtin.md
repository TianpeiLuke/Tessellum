---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - memory_builtin
keywords:
  - openclaw builtin memory engine
  - sqlite memory backend
  - fts5 keyword search bm25
  - vector hybrid search embeddings
  - sqlite-vec acceleration
  - cjk trigram tokenization
  - memorysearch provider config
  - openclaw memory index force
  - openclaw memory status deep
  - local gguf embeddings llama.cpp
topics:
  - OpenClaw
  - Memory Backend
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/memory-builtin
access_control_group: ["general"]
---

# OpenClaw — Builtin (SQLite) Memory Engine

## Overview

This note is the operator procedure for OpenClaw's **builtin memory engine**, the default memory backend, mirroring the `concepts/memory-builtin` source page. The builtin engine stores the memory index in a per-agent SQLite database and needs no extra dependencies to get started. It provides keyword search (FTS5/BM25), vector search (embeddings from any supported provider), and hybrid search that combines both, plus CJK trigram tokenization and optional sqlite-vec acceleration. This note walks through what it provides, getting started (OpenAI-default vs. explicit-provider vs. local-GGUF embeddings), the supported embedding-provider table, how indexing works, when to use it versus QMD or Honcho, and troubleshooting via `openclaw memory status`. Deeper config tuning is delegated to `reference/memory-config` and is linked rather than reproduced here.

## What it provides

The builtin engine is the default memory backend and offers the following retrieval capabilities, copied verbatim from the source page:

- **Keyword search** via FTS5 full-text indexing (BM25 scoring).
- **Vector search** via embeddings from any supported provider.
- **Hybrid search** that combines both for best results.
- **CJK support** via trigram tokenization for Chinese, Japanese, and Korean.
- **sqlite-vec acceleration** for in-database vector queries (optional).

## Getting started

By default, the builtin engine uses OpenAI embeddings. If you already have `OPENAI_API_KEY` or `models.providers.openai.apiKey` configured, vector search works with no extra memory config. Without an embedding provider, only keyword search is available.

To set a provider explicitly, configure `agents.defaults.memorySearch.provider`:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",
      },
    },
  },
}
```

To force local GGUF embeddings, install the official llama.cpp provider plugin, then point `local.modelPath` at a GGUF file:

```bash
openclaw plugins install @openclaw/llama-cpp-provider
```

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "local",
        fallback: "none",
        local: {
          modelPath: "~/.node-llama-cpp/models/embeddinggemma-300m-qat-Q8_0.gguf",
        },
      },
    },
  },
}
```

## Supported embedding providers

Set `memorySearch.provider` to switch away from OpenAI. The page lists the supported embedding providers with their config IDs and notes:

| Provider          | ID                  | Notes                               |
| ----------------- | ------------------- | ----------------------------------- |
| Bedrock           | `bedrock`           | Uses AWS credential chain           |
| DeepInfra         | `deepinfra`         | Default: `BAAI/bge-m3`              |
| Gemini            | `gemini`            | Supports multimodal (image + audio) |
| GitHub Copilot    | `github-copilot`    | Uses Copilot subscription           |
| Local             | `local`             | `@openclaw/llama-cpp-provider`      |
| Mistral           | `mistral`           |                                     |
| Ollama            | `ollama`            | Local/self-hosted                   |
| OpenAI            | `openai`            | Default: `text-embedding-3-small`   |
| OpenAI-compatible | `openai-compatible` | Generic `/v1/embeddings` endpoint   |
| Voyage            | `voyage`            |                                     |

## How indexing works

OpenClaw indexes `MEMORY.md` and `memory/*.md` into chunks (~400 tokens with 80-token overlap) and stores them in a per-agent SQLite database. The indexing mechanics are:

- **Index location:** the owning agent database at `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`
- **Storage maintenance:** SQLite WAL sidecars are bounded with periodic and shutdown checkpoints.
- **File watching:** changes to memory files trigger a debounced reindex (1.5s).
- **Auto-reindex:** when the embedding provider, model, or chunking config changes, the entire index is rebuilt automatically.
- **Reindex on demand:** `openclaw memory index --force`

You can also index Markdown files outside the workspace with `memorySearch.extraPaths` (see the configuration reference's additional-memory-paths section).

## When to use

The builtin engine is the right choice for most users:

- Works out of the box with no extra dependencies.
- Handles keyword and vector search well.
- Supports all embedding providers.
- Hybrid search combines the best of both retrieval approaches.

Consider switching to QMD (`/concepts/memory-qmd`) if you need reranking, query expansion, or want to index directories outside the workspace. Consider Honcho (`/concepts/memory-honcho`) if you want cross-session memory with automatic user modeling.

## Troubleshooting

The source page gives four diagnostic checks, all rooted in `openclaw memory status`:

- **Memory search disabled?** Check `openclaw memory status`. If no provider is detected, set one explicitly or add an API key.
- **Local provider not detected?** Confirm the local path exists and run `openclaw memory status --deep --agent main` then `openclaw memory index --force --agent main`. Both standalone CLI commands and the Gateway use the same `local` provider id; set `memorySearch.provider: "local"` when you want local embeddings.
- **Stale results?** Run `openclaw memory index --force` to rebuild. The watcher may miss changes in rare edge cases.
- **sqlite-vec not loading?** OpenClaw falls back to in-process cosine similarity automatically. `openclaw memory status --deep` reports the local vector store separately from the embedding provider, so `Vector store: unavailable` points at sqlite-vec loading while `Embeddings: unavailable` points at provider/auth or model readiness. Check logs for the specific load error.

The deep status command is:

```bash
openclaw memory status --deep --agent main
```

## Configuration

For embedding provider setup, hybrid search tuning (weights, MMR, temporal decay), batch indexing, multimodal memory, sqlite-vec, extra paths, and all other config knobs, the source page points to the Memory configuration reference (`/reference/memory-config`) rather than enumerating them inline.

**Source**: OpenClaw documentation — `concepts/memory-builtin` (mirror `inbox/openclaw_docs/concepts/memory-builtin.md`)
**Last Updated**: 2026-06-22
**Status**: Active
