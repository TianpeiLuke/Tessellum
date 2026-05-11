---
tags:
  - resource
  - terminology
  - llm_serving
  - memory_management
  - attention_mechanism
  - gpu_optimization
keywords:
  - KV cache
  - key-value cache
  - attention cache
  - LLM inference
  - autoregressive decoding
  - memory bottleneck
  - PagedAttention
topics:
  - LLM Inference Systems
  - Memory Management
  - Attention Mechanisms
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
related_wiki: null
---

# KV Cache - Key-Value Cache

## Definition

The **KV Cache** (Key-Value Cache) is a memory optimization technique used during autoregressive inference in transformer-based large language models. During text generation, each new token must attend to all previous tokens via the attention mechanism, which requires computing key (K) and value (V) projection vectors for every prior token at every layer and attention head. Rather than recomputing these projections from scratch at each generation step, the KV cache stores them incrementally — each step only computes K and V for the new token and appends them to the cache.

The KV cache is the primary memory bottleneck in LLM serving. For a model with `L` layers, `H` attention heads, and head dimension `d`, the KV cache for a single sequence of length `n` requires `2 × L × H × d × n` elements (the factor of 2 accounts for both keys and values). For large models like LLaMA-70B with long sequences, this can consume tens of gigabytes of GPU memory per request, often exceeding the memory required for the model weights themselves.

## Context

The KV cache is central to every LLM inference system, including vLLM, TensorRT-LLM, FasterTransformer, and Hugging Face Transformers. It appears at the intersection of model architecture and systems engineering:

- **Model side**: The attention mechanism in every transformer layer reads from and writes to the KV cache
- **Systems side**: Memory management of the KV cache (allocation, fragmentation, sharing) determines serving throughput
- **Optimization techniques**: Grouped-query attention (GQA), multi-query attention (MQA), KV cache quantization, and PagedAttention all target KV cache efficiency from different angles

In the buyer abuse prevention context, any system deploying LLM-based classifiers or reasoning agents (e.g., GreenTEA, SOPA, SPOT-X) must manage KV cache memory to achieve acceptable throughput and latency.

## Key Characteristics

- **Linear growth**: KV cache size grows linearly with sequence length — doubling the context window doubles the memory requirement
- **Per-request allocation**: Each concurrent request maintains its own KV cache, so batch size is directly limited by available GPU memory
- **Dynamic lifetime**: The cache grows token-by-token during generation and is released when the request completes; the final size is unknown at allocation time
- **Layer-wise storage**: Keys and values are cached independently at every transformer layer, creating a 3D structure (layers × heads × sequence length)
- **Fragmentation problem**: Naive contiguous allocation wastes 60-80% of memory due to internal fragmentation (reserving max length), external fragmentation (variable-length gaps), and redundant duplication (shared prefixes copied per request)
- **Compression variants**: Multi-query attention (MQA) shares KV across heads; grouped-query attention (GQA) shares within groups; KV cache quantization reduces precision from FP16 to INT8/INT4

## Related Terms

- **[LLM](term_llm.md)**: Large language models are the primary consumers of KV cache during inference
- **[LRU Cache](term_lru_cache.md)**: LRU eviction policy applied to KV cache management in long-context transformers; determines which key-value pairs to discard when cache capacity is exceeded
- **[Attention Mechanism](term_attention_mechanism.md)**: The computation that reads from the KV cache to produce attention-weighted outputs
- **[Self-Attention](term_self_attention.md)**: The specific attention variant where queries, keys, and values all derive from the same sequence
- **[Multi-Head Attention](term_multi_head_attention.md)**: Parallel attention heads, each maintaining independent KV cache entries
- **[Transformer](term_transformer.md)**: The architecture that introduced the attention mechanism and KV cache pattern
- **[Embedding](term_embedding.md)**: Input embeddings are projected into key, value, and query vectors that populate the KV cache
- **[vLLM](term_vllm.md)**: LLM serving engine that uses PagedAttention to manage KV cache with near-zero memory waste
- **[Inference Scaling Law](term_inference_scaling_law.md)**: Scaling laws for inference compute, where KV cache memory is a key constraint
- **[Gist Token](term_gist_token.md)**: Gist tokens compress cached KV entries into fewer virtual tokens, reducing KV cache memory footprint
- **[Block Masking](term_block_masking.md)**: Block masking physically evicts contiguous KV cache blocks for expired or irrelevant context, reclaiming GPU memory
- **[Cache Invalidation](term_cache_invalidation.md)**: Invalidation of stale KV entries in LLM inference affects generation quality, analogous to cache invalidation in distributed systems
- **[Cache Stampede](term_cache_stampede.md)**: KV cache shares the concept of cache pressure and memory management under concurrent access with distributed caching stampede scenarios
- **[Caching](term_caching.md)**: Parent concept; KV caching in transformers applies the same cache-hit/miss principles as infrastructure caching but optimized for attention computation
- **[Eviction Policy](term_eviction_policy.md)**: Eviction policies determine which context tokens are dropped when the KV cache exceeds GPU memory, paralleling cache eviction in distributed systems
- **[NGINX](term_nginx.md)**: NGINX's proxy cache is a system-level key-value cache for HTTP responses; KV Cache is a GPU-level key-value cache for attention computations — both trade memory for repeated computation
- **[Redis](term_redis.md)**: Redis is a production KV cache for application-layer key-value storage; conceptually related to transformer KV caches but operates at a different system layer (network vs. GPU memory)
- **[REST](term_rest.md)**: REST APIs leverage HTTP-level KV caching (CDN/proxy caches keyed by URL) while LLM KV caches store attention state — both are key-value stores optimizing repeated access patterns
- **[Session Persistence](term_session_persistence.md)**: Both KV cache and session persistence store stateful data keyed by identifier — KV cache stores attention state keyed by token position, session persistence stores user state keyed by session ID
- **[Write-Back Cache](term_write_back_cache.md)**: KV cache in LLM inference is conceptually write-back — attention keys and values are computed and cached in GPU memory, never written to persistent storage
- **[Write-Through Cache](term_write_through_cache.md)**: Unlike write-through caching which persists to a backing store, KV cache entries exist only in GPU memory and are discarded after request completion

## References

- [PagedAttention paper — Kwon et al., SOSP 2023](https://arxiv.org/abs/2309.06180)
- [vLLM GitHub Repository](https://github.com/vllm-project/vllm)
- [Attention Is All You Need — Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)
