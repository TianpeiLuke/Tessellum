---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - memory_config
keywords:
  - openclaw memory search config
  - memorysearch embedding provider
  - memorysearch.query.hybrid
  - embedding provider model fallback
  - api key resolution embeddings
  - openai-compatible embeddings endpoint
  - bedrock titan embedding config
  - multimodal memory gemini
  - session memory search experimental
  - embedding batch indexing
topics:
  - OpenClaw
  - Memory Search Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/memory-config
access_control_group: ["general"]
---

# OpenClaw — Memory Search & Embedding Configuration Reference

## Overview

This note is the operational procedure for configuring OpenClaw memory **search**: the embedding-provider/model/fallback selection, remote and provider-specific endpoint config, custom provider ids, per-provider API-key resolution, hybrid search (BM25 + vector + MMR + temporal decay), additional memory paths, multimodal (Gemini) indexing, the embedding cache, batch indexing, and experimental session-memory search. It mirrors the search/embedding half of the `reference/memory-config` source page. Unless noted otherwise, all settings here live under `agents.defaults.memorySearch` in `openclaw.json`. The reciprocal storage/backend knobs (sqlite-vec, index storage, the QMD backend, Dreaming) are split into the sibling note [oc_reference_memory_config_storage](oc_reference_memory_config_storage.md); the conceptual pipeline this config operationalizes is [oc_concepts_memory_search](oc_concepts_memory_search.md).

## Provider selection

Provider selection lives under `memorySearch` with four keys. `provider` (`string`, default `"openai"`) is the embedding adapter ID — one of `bedrock`, `deepinfra`, `gemini`, `github-copilot`, `local`, `mistral`, `ollama`, `openai`, `openai-compatible`, or `voyage` — and may also be a configured `models.providers.<id>` whose `api` points at a memory embedding adapter or OpenAI-compatible model API. `model` (`string`, default = provider default) is the embedding model name. `fallback` (`string`, default `"none"`) is the fallback adapter ID used when the primary fails. `enabled` (`boolean`, default `true`) enables or disables memory search. When `provider` is not set, OpenClaw uses OpenAI embeddings; set it explicitly to use Gemini, Voyage, Mistral, DeepInfra, Bedrock, GitHub Copilot, Ollama, a local GGUF model, or an OpenAI-compatible `/v1/embeddings` endpoint. Legacy configs that still say `provider: "auto"` resolve to `openai`.

**Index-identity warning.** Changing the embedding provider, model, provider settings, sources, scope, chunking, or tokenizer can make the existing SQLite vector index incompatible. OpenClaw pauses vector search and reports an index identity warning instead of automatically re-embedding everything. Rebuild when ready with `openclaw memory status --index --agent <id>` or `openclaw memory index --force --agent <id>`.

**FTS-only fallback and fail-closed semantics.** When `provider` is unset, legacy `provider: "auto"` is present, or `provider: "none"` intentionally selects FTS-only mode, memory recall can still use lexical FTS ranking when embeddings are unavailable. By contrast, explicit non-local providers fail closed: if you set `memorySearch.provider` to a concrete remote-backed provider (OpenAI, Gemini, Voyage, Mistral, Bedrock, GitHub Copilot, DeepInfra, Ollama, LM Studio, or an OpenAI-compatible custom provider) and that provider is unavailable at runtime, `memory_search` returns an unavailable result instead of silently falling back to FTS-only recall. Fix the provider/auth config, switch to a reachable provider, or set `provider: "none"` for deliberate FTS-only recall.

### Custom provider ids

`memorySearch.provider` can point at a custom `models.providers.<id>` entry for memory-specific provider adapters such as `ollama`, or for OpenAI-compatible model APIs such as `openai-responses` / `openai-completions`. OpenClaw resolves that provider's `api` owner for the embedding adapter while preserving the custom provider id for endpoint, auth, and model-prefix handling. This lets multi-GPU or multi-host setups dedicate memory embeddings to a specific local endpoint:

```json5
{
  models: {
    providers: {
      "ollama-5080": {
        api: "ollama",
        baseUrl: "http://gpu-box.local:11435",
        apiKey: "ollama-local",
        models: [{ id: "qwen3-embedding:0.6b" }],
      },
    },
  },
  agents: {
    defaults: {
      memorySearch: {
        provider: "ollama-5080",
        model: "qwen3-embedding:0.6b",
      },
    },
  },
}
```

### API key resolution

Remote embeddings require an API key; Bedrock uses the AWS SDK default credential chain instead (instance roles, SSO, access keys). The env var vs config key per provider:

| Provider       | Env var                                            | Config key                          |
| -------------- | -------------------------------------------------- | ----------------------------------- |
| Bedrock        | AWS credential chain                               | No API key needed                   |
| DeepInfra      | `DEEPINFRA_API_KEY`                                | `models.providers.deepinfra.apiKey` |
| Gemini         | `GEMINI_API_KEY`                                   | `models.providers.google.apiKey`    |
| GitHub Copilot | `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN` | Auth profile via device login       |
| Mistral        | `MISTRAL_API_KEY`                                  | `models.providers.mistral.apiKey`   |
| Ollama         | `OLLAMA_API_KEY` (placeholder)                     | --                                  |
| OpenAI         | `OPENAI_API_KEY`                                   | `models.providers.openai.apiKey`    |
| Voyage         | `VOYAGE_API_KEY`                                   | `models.providers.voyage.apiKey`    |

Codex OAuth covers chat/completions only and does not satisfy embedding requests. The `${ENV}` placeholder wiring shown below follows the [oc_reference_secret_placeholder_conventions](oc_reference_secret_placeholder_conventions.md) doc-hygiene rules.

## Remote endpoint config

Use `provider: "openai-compatible"` for a generic OpenAI-compatible `/v1/embeddings` server that should not inherit global OpenAI chat credentials. Three `remote.*` fields configure it: `remote.baseUrl` (`string`) is the custom API base URL, `remote.apiKey` (`string`) overrides the API key, and `remote.headers` (`object`) adds extra HTTP headers (merged with provider defaults).

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai-compatible",
        model: "text-embedding-3-small",
        remote: {
          baseUrl: "https://api.example.com/v1/",
          apiKey: "YOUR_KEY",
        },
      },
    },
  },
}
```

## Provider-specific config

**Gemini.** `model` (`string`, default `gemini-embedding-001`) also supports `gemini-embedding-2-preview`; `outputDimensionality` (`number`, default `3072`) for Embedding 2 accepts `768`, `1536`, or `3072`. Changing `model` or `outputDimensionality` changes the index identity, so OpenClaw pauses vector search until you explicitly rebuild the memory index.

**OpenAI-compatible input types.** OpenAI-compatible embedding endpoints can opt into provider-specific `input_type` request fields, useful for asymmetric embedding models that label query and document embeddings differently. `inputType` (`string`, unset) is the shared `input_type` for both; `queryInputType` (`string`, unset) is the query-time `input_type` and overrides `inputType`; `documentInputType` (`string`, unset) is the index/document `input_type` and overrides `inputType`. Changing these values affects embedding-cache identity for provider batch indexing and should be followed by a memory reindex when the upstream model treats the labels differently.

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai-compatible",
        remote: {
          baseUrl: "https://embeddings.example/v1",
          apiKey: "${EMBEDDINGS_API_KEY}",
        },
        model: "asymmetric-embedder",
        queryInputType: "query",
        documentInputType: "passage",
      },
    },
  },
}
```

**Bedrock.** Bedrock uses the AWS SDK default credential chain — no API keys needed. On EC2 with a Bedrock-enabled instance role, just set the provider and model:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "bedrock",
        model: "amazon.titan-embed-text-v2:0",
      },
    },
  },
}
```

`model` (`string`, default `amazon.titan-embed-text-v2:0`) accepts any Bedrock embedding model ID; `outputDimensionality` (`number`, default = model default) for Titan V2 accepts `256`, `512`, or `1024`. Supported models with family detection and dimension defaults: `amazon.titan-embed-text-v2:0` (Amazon, 1024 default, configurable 256/512/1024), `amazon.titan-embed-text-v1` (1536), `amazon.titan-embed-g1-text-02` (1536), `amazon.titan-embed-image-v1` (1024), `amazon.nova-2-multimodal-embeddings-v1:0` (1024 default, configurable 256/384/1024/3072), `cohere.embed-english-v3` (1024), `cohere.embed-multilingual-v3` (1024), `cohere.embed-v4:0` (1536 default, configurable 256-1536), `twelvelabs.marengo-embed-3-0-v1:0` (512), and `twelvelabs.marengo-embed-2-7-v1:0` (1024). Throughput-suffixed variants (e.g., `amazon.titan-embed-text-v1:2:8k`) inherit the base model's configuration. Bedrock auth uses the standard AWS SDK credential resolution order: (1) environment variables (`AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`), (2) SSO token cache, (3) web identity token credentials, (4) shared credentials and config files, (5) ECS or EC2 metadata credentials. Region resolves from `AWS_REGION`, `AWS_DEFAULT_REGION`, the `amazon-bedrock` provider `baseUrl`, or defaults to `us-east-1`. The IAM role/user needs `bedrock:InvokeModel` with `Effect: Allow` on `Resource: "*"`; for least-privilege, scope `InvokeModel` to the specific model ARN `arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v2:0`.

**Local (GGUF + llama.cpp).** `local.modelPath` (`string`, default auto-downloaded) is the path to the GGUF model file; `local.modelCacheDir` (`string`, default = node-llama-cpp default) is the cache dir for downloaded models; `local.contextSize` (`number | "auto"`, default `4096`) is the embedding context window — `4096` covers typical chunks (128–512 tokens) while bounding non-weight VRAM, lower to 1024–2048 on constrained hosts, and `"auto"` uses the model's trained maximum (not recommended for 8B+ models: Qwen3-Embedding-8B at 40 960 tokens needs ~32 GB VRAM vs ~8.8 GB at 4096). Install the official provider first with `openclaw plugins install @openclaw/llama-cpp-provider`; the default model is `embeddinggemma-300m-qat-Q8_0.gguf` (~0.6 GB, auto-downloaded), and source checkouts still require native build approval (`pnpm approve-builds` then `pnpm rebuild node-llama-cpp`). Verify the same provider path the Gateway uses with `openclaw memory status --deep --agent main` and `openclaw memory index --force --agent main`. Set `provider: "local"` explicitly for local GGUF embeddings; `hf:` and HTTP(S) model references are supported for explicit local configs but do not change the default provider.

### Inline embedding timeout

`sync.embeddingBatchTimeoutSeconds` (`number`) overrides the timeout for inline embedding batches during memory indexing. Unset uses the provider default: 600 seconds for local/self-hosted providers such as `local`, `ollama`, and `lmstudio`, and 120 seconds for hosted providers. Increase it when local CPU-bound embedding batches are healthy but slow.

## Hybrid search config

All hybrid-search knobs live under `memorySearch.query.hybrid`: `enabled` (`boolean`, default `true`) enables hybrid BM25 + vector search; `vectorWeight` (`number`, default `0.7`) weights vector scores (0-1); `textWeight` (`number`, default `0.3`) weights BM25 scores (0-1); `candidateMultiplier` (`number`, default `4`) is the candidate-pool size multiplier. **MMR (diversity):** `mmr.enabled` (`boolean`, default `false`) enables MMR re-ranking and `mmr.lambda` (`number`, default `0.7`) sets the trade-off (0 = max diversity, 1 = max relevance). **Temporal decay (recency):** `temporalDecay.enabled` (`boolean`, default `false`) enables a recency boost and `temporalDecay.halfLifeDays` (`number`, default `30`) is how many days for the score to halve. Evergreen files (`MEMORY.md`, non-dated files in `memory/`) are never decayed.

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        query: {
          hybrid: {
            vectorWeight: 0.7,
            textWeight: 0.3,
            mmr: { enabled: true, lambda: 0.7 },
            temporalDecay: { enabled: true, halfLifeDays: 30 },
          },
        },
      },
    },
  },
}
```

## Additional memory paths

`extraPaths` (`string[]`) lists additional directories or files to index, e.g. `extraPaths: ["../team-docs", "/srv/shared-notes"]` under `agents.defaults.memorySearch`. Paths can be absolute or workspace-relative; directories are scanned recursively for `.md` files. Symlink handling depends on the active backend: the builtin engine ignores symlinks, while QMD follows the underlying QMD scanner behavior. For agent-scoped cross-agent transcript search, use `agents.list[].memorySearch.qmd.extraCollections` instead of `memory.qmd.paths`; those extra collections follow the same `{ path, name, pattern? }` shape, are merged per agent, and can preserve explicit shared names when the path points outside the current workspace. If the same resolved path appears in both `memory.qmd.paths` and `memorySearch.qmd.extraCollections`, QMD keeps the first entry and skips the duplicate.

## Multimodal memory (Gemini)

Index images and audio alongside Markdown using Gemini Embedding 2. `multimodal.enabled` (`boolean`, default `false`) enables multimodal indexing; `multimodal.modalities` (`string[]`) accepts `["image"]`, `["audio"]`, or `["all"]`; `multimodal.maxFileBytes` (`number`, default `10000000`) is the max file size for indexing. This only applies to files in `extraPaths` — default memory roots stay Markdown-only — and requires `gemini-embedding-2-preview` with `fallback` set to `"none"`. Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.heic`, `.heif` (images); `.mp3`, `.wav`, `.ogg`, `.opus`, `.m4a`, `.aac`, `.flac` (audio).

## Embedding cache

`cache.enabled` (`boolean`, default `true`) caches chunk embeddings in SQLite; `cache.maxEntries` (`number`, default `50000`) caps the number of cached embeddings. The cache prevents re-embedding unchanged text during reindex or transcript updates.

## Batch indexing

Batch-indexing knobs: `remote.nonBatchConcurrency` (`number`, default `4`) sets parallel inline embeddings; `remote.batch.enabled` (`boolean`, default `false`) enables the batch embedding API; `remote.batch.concurrency` (`number`, default `2`) sets parallel batch jobs; `remote.batch.wait` (`boolean`, default `true`) waits for batch completion; `remote.batch.pollIntervalMs` (`number`) is the poll interval; `remote.batch.timeoutMinutes` (`number`) is the batch timeout. Batch is available for `openai`, `gemini`, and `voyage`; OpenAI batch is typically fastest and cheapest for large backfills. `remote.nonBatchConcurrency` controls inline embedding calls used by local/self-hosted providers and by hosted providers when provider batch APIs are not active — Ollama defaults to `1` for non-batch indexing to avoid overwhelming smaller local hosts, so raise it on larger machines. This is separate from `sync.embeddingBatchTimeoutSeconds`, which controls the timeout for inline embedding calls.

## Session memory search (experimental)

Index session transcripts and surface them via `memory_search`. `experimental.sessionMemory` (`boolean`, default `false`) enables session indexing; `sources` (`string[]`, default `["memory"]`) adds `"sessions"` to include transcripts; `sync.sessions.deltaBytes` (`number`, default `100000`) is the byte threshold for reindex; `sync.sessions.deltaMessages` (`number`, default `50`) is the message threshold for reindex. Session indexing is opt-in and runs asynchronously, so results can be slightly stale; session logs live on disk, so treat filesystem access as the trust boundary.

**Source**: OpenClaw documentation — `reference/memory-config` (mirror `inbox/openclaw_docs/reference/memory-config.md`)
**Last Updated**: 2026-06-22
**Status**: Active
