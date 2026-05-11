---
tags:
  - resource
  - terminology
  - kv_cache
  - efficient_inference
  - attention_mechanism
  - structured_sparsity
keywords:
  - block masking
  - KV cache eviction
  - block-level attention
  - structured sparsity
  - PagedAttention
  - PagedEviction
  - KV cache pruning
  - reasoning chain compression
topics:
  - Efficient Inference
  - Attention Mechanisms
  - KV Cache Management
language: markdown
date of note: 2026-04-18
status: active
building_block: concept
related_wiki: null
---

# Block Masking

## Definition

**Block masking** is an inference-time technique that physically removes contiguous blocks of KV cache entries from GPU memory after they have been summarized or deemed no longer necessary. Unlike standard attention masking (which zeros out attention weights but retains all KV entries in memory), block masking reclaims memory immediately, enabling real KV cache reduction and increased serving throughput.

The technique was introduced in the MEMENTO framework (Kontonis et al., 2026) for reasoning chain compression: after a reasoning block is completed and summarized into a memento, the block's KV entries are evicted from the cache. Future tokens attend only to the memento text and residual KV states, not the full original block.

## Context

Block masking sits at the intersection of two trends in LLM inference optimization:

1. **Structured KV cache management**: Systems like vLLM use PagedAttention to manage KV cache in fixed-size blocks (pages). Block masking aligns with this block structure — evicting entire pages rather than individual tokens
2. **Self-managed context compression**: Rather than external tools deciding what to evict (attention-score-based pruning), MEMENTO's block masking is triggered by the model itself when it generates a `<|summary_end|>` token

The broader research area includes PagedEviction (structured block-wise pruning), KV-Compress (variable compression rates per attention head), and Zipage (compressed PagedAttention for reasoning), all of which address the same fundamental problem: reducing KV cache memory consumption without degrading output quality.

## Key Characteristics

- **Physical eviction, not masking**: Standard attention masks set attention weights to zero but keep KV entries in GPU memory. Block masking actually frees the memory, enabling real throughput gains
- **Block-level granularity**: Operates on contiguous chunks of tokens (reasoning blocks of hundreds to thousands of tokens), not individual tokens — simpler than per-token eviction decisions
- **Model-triggered**: In MEMENTO, eviction is triggered by the model generating a special token (`<|summary_end|>`), giving the model control over when to compress
- **PagedAttention compatible**: Implemented as a vLLM extension that integrates with the existing PagedAttention block-based memory manager
- **Enables RL training**: The vLLM block masking extension supports both inference and reinforcement learning rollouts, enabling CISPO training
- **~2.5x peak KV cache reduction**: In MEMENTO experiments across Qwen3 and Phi-4 models
- **~1.75x throughput improvement**: From both reduced memory (fitting more sequences) and reduced attention computation

## Comparison with Related KV Cache Optimization Approaches

| Method | Granularity | Trigger | Memory Freed? | Quality Impact |
|--------|-------------|---------|---------------|----------------|
| **Attention masking** | Token-level | Static pattern | No (weights zeroed, KV retained) | None |
| **Block masking (MEMENTO)** | Block-level | Model-generated token | Yes (physical eviction) | Modest (2.6-6.3pp) |
| **PagedEviction** | Block-level | Attention score proxy | Yes (page eviction) | Variable |
| **KV-Compress** | Block-level | Importance scoring | Yes (proportional) | Up to 5.18x throughput |
| **Zipage** | Token-level + paging | Scheduling strategy | Yes (compressed pages) | Close to full KV |
| **Sliding window** | Fixed window | Position-based | Yes (old tokens dropped) | Degrades for long-range dependencies |
| **Gist tokens** | Token-level | Learned compression | Partial (fewer tokens) | Minimal at low ratios |

## Limitations

- **Requires model cooperation**: MEMENTO's block masking only works with models fine-tuned to generate block boundaries and summaries — cannot be applied to arbitrary models
- **Fixed block boundaries**: Once a block is evicted, the decision is irreversible — if the summary was inadequate, information is permanently lost
- **Dual information stream**: Probing experiments show masked blocks retain information in implicit KV states (23-27% passcode recovery), suggesting eviction is not complete at the representation level
- **Custom infrastructure**: Requires a modified vLLM fork — not available in standard serving frameworks
- **Not adaptive**: Cannot adjust compression aggressiveness per-block based on content difficulty

## Related Terms

- **[KV Cache](term_kv_cache.md)**: Block masking directly targets KV cache memory by evicting completed reasoning blocks, achieving ~2.5x peak reduction
- **[Attention Mechanism](term_attention_mechanism.md)**: Block masking creates a structured sparse attention pattern where future tokens attend only to summaries, not original blocks
- **[vLLM](term_vllm.md)**: The MEMENTO block masking extension is built on vLLM's PagedAttention infrastructure, physically freeing page blocks
- **[Flash Attention](term_flash_attention.md)**: Complementary optimization — Flash Attention accelerates the attention kernel, while block masking reduces the number of KV entries to process
- **[Gist Token](term_gist_token.md)**: Alternative compression approach — gist tokens compress via learned latent vectors; block masking compresses via text summaries + KV eviction
- **[CISPO](term_cispo.md)**: RL algorithm that uses the block masking vLLM extension for training rollouts
- **[Context Engineering](term_context_engineering.md)**: Block masking is a self-managed context compression technique within the broader context engineering paradigm
- **[Linear Attention](term_linear_attention.md)**: Alternative approach to reducing attention cost — linear attention replaces softmax with linear kernels; block masking keeps standard attention but reduces the sequence length
- **[Self Attention](term_self_attention.md)**: Block masking modifies the self-attention pattern by restricting which positions can attend to which
- **[Progressive Summarization](term_progressive_summarization.md)**: Conceptual parallel — block masking progressively compresses context as reasoning progresses, similar to progressive summarization in knowledge management

## References

- [Kontonis et al. (2026). "MEMENTO: Teaching LLMs to Manage Their Own Context." arXiv:2604.09852](https://arxiv.org/abs/2604.09852)
- [MEMENTO (Kontonis et al., 2026)](../papers/lit_kontonis2026memento.md) — introduces block masking for reasoning chain compression
- [PagedEviction: Structured Block-wise KV Cache Pruning (2025)](https://arxiv.org/abs/2509.04377)
- [Zipage: Compressed PagedAttention for LLM Reasoning (2026)](https://arxiv.org/abs/2603.08743)
- [KV-Compress: Paged KV-Cache Compression with Variable Rates (2024)](https://arxiv.org/abs/2410.00161)
