---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - local_inference
keywords:
  - local LLM on Mac
  - llama.cpp server
  - MLX omlx
  - quantized KV cache
  - Apple Silicon inference
  - OpenAI-compatible endpoint
topics:
  - Hermes Agent
  - Providers & Setup
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac
access_control_group: ["general"]
---

# Run Local LLMs on Mac

## Overview

This is the task script for running a **local, OpenAI-compatible LLM server on macOS** and pointing Hermes at it — giving you full privacy, zero API cost, and surprisingly strong performance on Apple Silicon (M1 and later). It covers two interchangeable backends, both of which expose an OpenAI-compatible `/v1/chat/completions` endpoint: **llama.cpp** (`brew install llama.cpp`, GGUF format, fastest time-to-first-token, quantized KV cache for low memory) and **omlx** (the [omlx.ai](https://omlx.ai) macOS app, MLX/safetensors format, fastest token generation via native Metal optimization). Because both speak the OpenAI wire format, Hermes connects to either via the `hermes model` Custom-endpoint picker — you just give it the base URL (`http://localhost:8080` for llama.cpp, `http://127.0.0.1:8000` for omlx) and the model name.

The page is fundamentally about **fitting a model into unified memory** (model size + KV cache) and then **choosing the right backend for your workload** (low-latency interactive vs. long-form throughput). Intel Macs work with llama.cpp but without GPU acceleration. Note: the `config.yaml` model/provider/`base_url` settings are owned by the model-config reference, and the streaming/timeout env-var master table lives in the env-var reference; this note documents only the local-setup procedure and the local-specific timeout auto-relaxation.

## Choosing a model

The recommended starter is **Qwen3.5-9B** — a strong reasoning model that fits comfortably in 8 GB+ of unified memory with quantization. Two variants:

| Variant | Size on disk | RAM needed (128K context) | Backend |
|---------|-------------|---------------------------|---------|
| Qwen3.5-9B-Q4_K_M (GGUF) | 5.3 GB | ~10 GB with quantized KV cache | llama.cpp |
| Qwen3.5-9B-mlx-lm-mxfp4 (MLX) | ~5 GB | ~12 GB | omlx |

**Memory rule of thumb: model size + KV cache.** A 9B Q4 model is ~5 GB. The KV cache at 128K context with Q4 quantization adds ~4–5 GB; with default (f16) KV cache it balloons to ~16 GB — which is why the quantized KV-cache flags in llama.cpp are the key trick for memory-constrained systems. Larger models (27B, 35B) need 32 GB+ of unified memory; the 9B is the sweet spot for 8–16 GB machines.

## Option A: llama.cpp

llama.cpp is the most portable local LLM runtime; on macOS it uses Metal for GPU acceleration out of the box. Install with `brew install llama.cpp` (gives you `llama-server` globally), then download a GGUF model via `huggingface-cli` (`huggingface-cli login` first if you hit a 401/404 on a gated model):

```bash
huggingface-cli download unsloth/Qwen3.5-9B-GGUF Qwen3.5-9B-Q4_K_M.gguf --local-dir ~/models
```

Start the server with the memory-tuned flag set:

```bash
llama-server -m ~/models/Qwen3.5-9B-Q4_K_M.gguf \
  -ngl 99 \
  -c 131072 \
  -np 1 \
  -fa on \
  --cache-type-k q4_0 \
  --cache-type-v q4_0 \
  --host 0.0.0.0
```

Key flags: `-ngl 99` offloads all layers to the GPU (Metal); `-c 131072` sets the 128K context window (reduce only if low on memory); `-np 1` keeps a single slot for single-user use (more slots split the memory budget); `-fa on` enables flash attention (cuts memory, speeds long-context inference); `--cache-type-k/v q4_0` quantize the key/value cache to 4-bit — **the big memory saver**, cutting KV-cache memory ~75% vs. f16; `--host 0.0.0.0` listens on all interfaces (use `127.0.0.1` if you don't need network access). The server is ready when it logs `main: server is listening on http://0.0.0.0:8080` and `all slots are idle`.

**Memory optimization for constrained systems.** The quantized-KV-cache flags dominate memory use at 128K context: f16 (default) ~16 GB, q8_0 ~8 GB, **q4_0 ~4 GB**. On an 8 GB Mac, use `q4_0` KV cache and pick a smaller model that still fits Hermes' **64K minimum context**. On 16 GB you can comfortably run 128K context; on 32 GB+ you can run larger models or multiple parallel slots. If still out of memory, reduce context only while staying at/above the 64K minimum — otherwise switch to a smaller model or smaller quantization (Q3_K_M instead of Q4_K_M).

Test it, then look up the served model name if you forget it:

```bash
curl -s http://localhost:8080/v1/models | jq '.data[].id'
```

## Option B: MLX via omlx

[omlx](https://omlx.ai) is a macOS-native app that manages and serves MLX models. MLX is Apple's own ML framework, optimized specifically for Apple Silicon's unified-memory architecture. **Install** by downloading from omlx.ai — it provides a GUI for model management plus a built-in server. **Download** by browsing within the app (search `Qwen3.5-9B-mlx-lm-mxfp4`; models land in `~/.omlx/models/`). **Start** serving from the app UI (or CLI if available); omlx serves on `http://127.0.0.1:8000` by default. Test it and list the (possibly multiple) served models the same OpenAI-compatible way:

```bash
curl -s http://127.0.0.1:8000/v1/models | jq '.data[].id'
```

## Benchmarks: llama.cpp vs MLX

Both backends were tested on the same machine (Apple M5 Max, 128 GB unified memory) running the same model (Qwen3.5-9B) at comparable quantization (Q4_K_M for GGUF, mxfp4 for MLX), five prompts × three runs, run sequentially to avoid contention.

| Metric | llama.cpp (Q4_K_M) | MLX (mxfp4) | Winner |
|--------|-------------------|-------------|--------|
| TTFT (avg) | **67 ms** | 289 ms | llama.cpp (4.3× faster) |
| TTFT (p50) | **66 ms** | 286 ms | llama.cpp (4.3× faster) |
| Generation (avg) | 70 tok/s | **96 tok/s** | MLX (37% faster) |
| Total time (512 tokens) | 7.3 s | **5.5 s** | MLX (25% faster) |

**What this means.** llama.cpp excels at prompt processing — its flash-attention + quantized-KV-cache pipeline returns the first token in ~66 ms, a meaningful edge for interactive apps (chatbots, autocomplete) where perceived responsiveness matters. MLX generates ~37% faster once going, finishing sooner on batch workloads, long-form generation, or any task where total completion time beats initial latency. Both are extremely consistent across runs. **Which to pick:** interactive chat / low-latency tools → llama.cpp; long-form / bulk → MLX (omlx); memory-constrained 8–16 GB → llama.cpp (quantized KV cache is unmatched); serving multiple models at once → omlx (built-in multi-model support); maximum compatibility (Linux too) → llama.cpp.

## Connect to Hermes

Once your local server is running, run the model picker, select **Custom endpoint**, and follow the prompts — it asks for the base URL and model name; use the values from whichever backend you set up above (the `model.provider`/`base_url` it writes are persisted to `config.yaml`):

```bash
hermes model
```

## Timeouts

Hermes **automatically detects local endpoints** (localhost, LAN IPs) and relaxes its streaming timeouts — no configuration needed for most setups. The stream-read timeout is the one most likely to bite: it is the socket-level deadline for receiving the next chunk, and during prefill on large contexts a local model may emit nothing for minutes while processing the prompt. Auto-detection handles this transparently, but you can override via `.env` (e.g. raise the 120 s default to 30 minutes):

```bash
# In your .env — raise from the 120s default to 30 minutes
HERMES_STREAM_READ_TIMEOUT=1800
```

| Timeout | Default | Local auto-adjustment | Env var override |
|---------|---------|----------------------|------------------|
| Stream read (socket-level) | 120 s | Raised to 1800 s | `HERMES_STREAM_READ_TIMEOUT` |
| Stale stream detection | 180 s | Disabled entirely | `HERMES_STREAM_STALE_TIMEOUT` |
| API call (non-streaming) | 1800 s | No change needed | `HERMES_API_TIMEOUT` |

**Source**: https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac
**Last Updated**: 2026-06-19
**Status**: Active
