---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - memory
keywords:
  - memory-lancedb plugin
  - openclaw long-term memory
  - lancedb vector store memory
  - openclaw embedding provider config
  - ollama embeddings openclaw
  - openclaw ltm cli
  - recallmaxchars capturemaxchars
  - plugins.slots.memory
  - openclaw memory dbpath storageoptions
topics:
  - OpenClaw
  - Memory Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/memory-lancedb
access_control_group: ["general"]
---

# OpenClaw — Configuring the `memory-lancedb` Vector-Store Memory Plugin

## Overview

This note is the procedure for installing and configuring `memory-lancedb`, OpenClaw's official external memory plugin that stores long-term memory in LanceDB and uses embeddings for recall — it can automatically recall relevant memories before a model turn and capture important facts after a response. It mirrors the `plugins/memory-lancedb` source page end to end: installation and memory-slot ownership, the quick-start config, the three embedding paths (provider-backed, Ollama, raw OpenAI-compatible), recall/capture limits, the `ltm` CLI namespace and agent memory tools, on-disk and S3 storage, the native runtime dependency, and troubleshooting. Use it when you want a local vector database for memory, need an OpenAI-compatible embedding endpoint, or want to keep a memory database outside the default built-in memory store.

## Installation

Install `memory-lancedb` BEFORE setting `plugins.slots.memory = "memory-lancedb"`:

```bash
openclaw plugins install @openclaw/memory-lancedb
```

The plugin is published to npm and is **not** bundled into the OpenClaw runtime image. The installer writes the plugin entry and switches the memory slot when no other plugin owns it. `memory-lancedb` is an *active memory plugin*: enable it by selecting the memory slot with `plugins.slots.memory = "memory-lancedb"`. Companion plugins such as `memory-wiki` can run beside it, but only one plugin owns the active memory slot.

## Quick Start

Set the memory slot and enable the plugin entry with a minimal embedding config and the auto-recall / auto-capture toggles:

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb",
    },
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            provider: "openai",
            model: "text-embedding-3-small",
          },
          autoRecall: true,
          autoCapture: false,
        },
      },
    },
  },
}
```

Restart the Gateway after changing plugin config with `openclaw gateway restart`, then verify the plugin is loaded with `openclaw plugins list`.

## Embedding Providers

`memory-lancedb` can use the same memory embedding provider adapters as `memory-core`. There are three configuration paths.

### Provider-backed embeddings

Set `embedding.provider` and **omit** `embedding.apiKey` to use the provider's configured auth profile, environment variable, or `models.providers.<provider>.apiKey`. This path works with provider auth profiles that expose embedding credentials. For example, GitHub Copilot can be used when the Copilot profile/plan supports embeddings (`embedding.provider: "github-copilot"`, `model: "text-embedding-3-small"`). One important caveat: OpenAI Codex / ChatGPT OAuth is **not** an OpenAI Platform embeddings credential — for OpenAI embeddings, use an OpenAI API key auth profile, `OPENAI_API_KEY`, or `models.providers.openai.apiKey`. OAuth-only users can use another embedding-capable provider such as GitHub Copilot or Ollama.

### Ollama embeddings

For Ollama embeddings, prefer the bundled Ollama embedding provider. It uses the native Ollama `/api/embed` endpoint and follows the same auth/base URL rules as the Ollama provider. Set `dimensions` for non-standard embedding models, and lower `recallMaxChars` for small local embedding models if you see context length errors from the local server:

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb",
    },
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            provider: "ollama",
            baseUrl: "http://127.0.0.1:11434",
            model: "mxbai-embed-large",
            dimensions: 1024,
          },
          recallMaxChars: 400,
          autoRecall: true,
          autoCapture: false,
        },
      },
    },
  },
}
```

OpenClaw knows the dimensions for `text-embedding-3-small` and `text-embedding-3-large`; custom models need the value in config so LanceDB can create the vector column.

### Raw OpenAI-compatible providers

Some OpenAI-compatible embedding providers reject the `encoding_format` parameter, while others ignore it and always return `number[]` vectors. `memory-lancedb` therefore omits `encoding_format` on embedding requests and accepts either float-array responses or base64-encoded float32 responses. If you have a raw OpenAI-compatible embeddings endpoint with no bundled provider adapter, omit `embedding.provider` (or leave it as `openai`) and set `embedding.apiKey` plus `embedding.baseUrl` — this preserves the direct OpenAI-compatible client path. Set `embedding.dimensions` for providers whose model dimensions are not built in; for example, ZhiPu `embedding-3` uses `2048` dimensions (`baseUrl: "https://open.bigmodel.cn/api/paas/v4"`, `apiKey: "${ZHIPU_API_KEY}"`).

## Recall and Capture Limits

`memory-lancedb` has separate text limits, all defaulted and range-bounded:

| Setting           | Default | Range     | Applies to                                                |
| ----------------- | ------- | --------- | --------------------------------------------------------- |
| `recallMaxChars`  | `1000`  | 100-10000 | text sent to the embedding API for recall                 |
| `captureMaxChars` | `500`   | 100-10000 | message length eligible for auto-capture                  |
| `customTriggers`  | `[]`    | 0-50      | literal phrases that make auto-capture consider a message |

`recallMaxChars` controls auto-recall, the `memory_recall` tool, the `memory_forget` query path, and `openclaw ltm search`. Auto-recall prefers the latest user message from the turn and falls back to the full prompt only when no user message is available, which keeps channel metadata and large prompt blocks out of the embedding request. `captureMaxChars` controls whether a response is short enough to be considered for automatic capture; it does **not** cap recall query embeddings. `customTriggers` lets you add literal auto-capture phrases without writing regular expressions — the built-in triggers include common English, Czech, Chinese, Japanese, and Korean memory phrases.

## Commands and Agent Tools

When `memory-lancedb` is the active memory plugin, it registers the `ltm` CLI namespace (`openclaw ltm list`, `openclaw ltm search "project preferences"`, `openclaw ltm stats`). The `query` subcommand runs a non-vector query against the LanceDB table directly:

```bash
openclaw ltm query --cols id,text,createdAt --limit 20
openclaw ltm query --filter "category = 'preference'" --order-by createdAt:desc
```

- `--cols <columns>`: comma-separated column allowlist (defaults to `id`, `text`, `importance`, `category`, `createdAt`).
- `--filter <condition>`: SQL-style WHERE clause; capped at 200 characters and restricted to alphanumerics, comparison operators, quotes, parentheses, and a small set of safe punctuation.
- `--limit <n>`: positive integer; default `10`.
- `--order-by <column>:<asc|desc>`: in-memory sort applied after the filter; the sort column is auto-included in the projection.

Agents also get LanceDB memory tools from the active memory plugin: `memory_recall` for LanceDB-backed recall, `memory_store` for saving important facts, preferences, decisions, and entities, and `memory_forget` for removing matching memories.

## Storage

By default, LanceDB data lives under `~/.openclaw/memory/lancedb`; override the path with `dbPath`. `storageOptions` accepts string key/value pairs for LanceDB storage backends and supports `${ENV_VAR}` expansion — for example, pointing `dbPath` at S3 (`s3://memory-bucket/openclaw`) with `access_key`, `secret_key`, and `endpoint` keys:

```json5
{
  plugins: {
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          dbPath: "s3://memory-bucket/openclaw",
          storageOptions: {
            access_key: "${AWS_ACCESS_KEY_ID}",
            secret_key: "${AWS_SECRET_ACCESS_KEY}",
            endpoint: "${AWS_ENDPOINT_URL}",
          },
          embedding: {
            apiKey: "${OPENAI_API_KEY}",
            model: "text-embedding-3-small",
          },
        },
      },
    },
  },
}
```

## Runtime Dependencies

`memory-lancedb` depends on the native `@lancedb/lancedb` package. Packaged OpenClaw treats that package as part of the plugin package. Gateway startup does **not** repair plugin dependencies; if the dependency is missing, reinstall or update the plugin package and restart the Gateway. If an older install logs a missing `dist/package.json` or missing `@lancedb/lancedb` error during plugin load, upgrade OpenClaw and restart the Gateway. If the plugin logs that LanceDB is unavailable on `darwin-x64`, use the default memory backend on that machine, move the Gateway to a supported platform, or disable `memory-lancedb`.

## Troubleshooting

**Input length exceeds the context length** — this usually means the embedding model rejected the recall query (`memory-lancedb: recall failed: Error: 400 the input length exceeds the context length`). Set a lower `recallMaxChars` (e.g. `400`), then restart the Gateway. For Ollama, also verify the embedding server is reachable from the Gateway host:

```bash
curl http://127.0.0.1:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"mxbai-embed-large","input":"hello"}'
```

**Unsupported embedding model** — without `dimensions`, only the built-in OpenAI embedding dimensions are known; for local or custom embedding models, set `embedding.dimensions` to the vector size reported by that model. **Plugin loads but no memories appear** — check that `plugins.slots.memory` points at `memory-lancedb`, then run `openclaw ltm stats` and `openclaw ltm search "recent preference"`. If `autoCapture` is disabled, the plugin will recall existing memories but will not automatically store new ones — use the `memory_store` tool or enable `autoCapture` if you want automatic capture.

**Source**: OpenClaw documentation — `plugins/memory-lancedb` (mirror `inbox/openclaw_docs/plugins/memory-lancedb.md`)
**Last Updated**: 2026-06-22
**Status**: Active
