---
tags:
  - resource
  - terminology
  - inference_optimization
  - large_language_models
  - transformer_architecture
  - parallel_computing
keywords:
  - speculative decoding
  - speculative sampling
  - draft model
  - verifier model
  - target model
  - inference acceleration
  - autoregressive generation
  - token verification
  - rejection sampling
  - EAGLE
  - Medusa
topics:
  - Inference Optimization
  - Large Language Models
  - Transformer Architecture
  - Parallel Computing
language: markdown
date of note: 2026-03-17
status: active
building_block: concept
---

# Speculative Decoding

## Definition

**Speculative decoding** is an inference optimization technique that accelerates autoregressive text generation from large language models (LLMs) by computing multiple tokens in parallel without affecting output quality. The method pairs a large, accurate **target model** (the verifier) with a smaller, faster **draft model** that speculatively generates candidate token sequences. The target model then verifies all draft tokens in a single forward pass using **rejection sampling**, accepting tokens whose probabilities under the target distribution meet the acceptance criterion and resampling from a corrected distribution when they do not.

The critical mathematical guarantee is that the output distribution of speculative decoding is **identical** to that of standard autoregressive decoding from the target model alone. This means the technique provides a pure latency optimization with zero quality degradation -- a rare property among inference acceleration methods.

The technique exploits two key observations: (1) many tokens in natural language are "easy" and predictable by smaller models, and (2) LLM inference on modern GPUs is **memory-bandwidth-bound** rather than compute-bound, leaving spare computational capacity that can be used for parallel verification.

## Historical Context

Speculative decoding was independently proposed by two research groups in late 2022 / early 2023:

| Milestone | Authors | Paper | Date |
|-----------|---------|-------|------|
| Original proposal | Leviathan, Kalman, Matias (Google Research) | "Fast Inference from Transformers via Speculative Decoding" (arXiv:2211.17192) | November 2022 |
| Concurrent independent work | Chen, Borgeaud, Irving et al. (DeepMind) | "Accelerating Large Language Model Decoding with Speculative Sampling" (arXiv:2302.01318) | February 2023 |
| Conceptual precursor | Stern et al. | Blockwise parallel decoding (restricted form) | 2018 |

The Google Research paper introduced the term "speculative decoding" and formalized the rejection sampling framework. The DeepMind paper independently developed the same core idea under the name "speculative sampling." Both papers demonstrated 2-3x speedups on translation and summarization tasks while maintaining identical output distributions.

Since 2023, speculative decoding has become a foundational inference optimization paradigm, spawning numerous variants and being adopted in production by Google (AI Overviews in Search), Meta, NVIDIA, and major LLM serving frameworks.

## Taxonomy

Speculative decoding methods are classified by how they generate draft tokens:

| Variant | Draft Mechanism | Key Property | Representative Work |
|---------|----------------|--------------|---------------------|
| **Draft-Model-Based** | Separate smaller model generates candidates sequentially | Clean separation; model-agnostic | Leviathan et al. (2022), Chen et al. (2023) |
| **Self-Speculative (SSD)** | Skip intermediate layers of the target model itself | No auxiliary model needed; single-model approach | Zhang et al. (2023) |
| **Medusa** | Multiple parallel decoding heads attached to target model's final layer | Self-distillation training; no separate model | Cai et al. (2024) |
| **EAGLE / EAGLE-2 / EAGLE-3** | Lightweight autoregressive head on target model's hidden states | Feature-level drafting; instance-adaptive tree generation | Li et al. (2024) |
| **Lookahead Decoding** | N-gram based speculation from Jacobi iteration | Training-free; no draft model | Fu et al. (2024) |
| **Staged Speculative Decoding** | Recursive speculation -- draft model itself uses a smaller draft | Multi-level drafting hierarchy | Spector & Re (2023) |
| **Multi-Token Prediction (MTP)** | Multiple specialized prediction heads (e.g., DeepSeek-R1) | Native integration during pretraining | DeepSeek (2024) |
| **Token Tree Verification** | Draft tokens organized as a tree; batch-verify all branches | Higher acceptance rate via branching | SpecInfer, SpecTr, Sequoia |

## Key Properties

- **Lossless acceleration**: Output distribution is mathematically identical to standard autoregressive decoding; no approximation or quality trade-off
- **Acceptance criterion**: Draft token x is accepted with probability min(1, p_target(x) / p_draft(x)); rejected tokens are resampled from a corrected distribution
- **Typical speedup**: 2-3x for well-matched draft-target pairs; up to 3.6x reported with TensorRT-LLM; Groq reports 6x on Llama-3.1-70B
- **Memory-bound exploitation**: Leverages the fact that LLM inference underutilizes GPU compute due to memory bandwidth bottleneck
- **Speculation length**: Typically 3-12 candidate tokens per draft step; optimal length depends on acceptance rate
- **Acceptance rate**: The fraction of draft tokens accepted by the verifier; directly determines speedup magnitude; higher when draft model closely matches target
- **At least one token per step**: Even if all draft tokens are rejected, the verifier always produces at least one valid token (from its own distribution), guaranteeing forward progress
- **KV cache efficiency**: Only new speculated tokens incur compute cost during verification; accepted tokens reuse cached key-value pairs

## Notable Systems / Implementations

| System / Framework | Speculative Method | Notes |
|--------------------|-------------------|-------|
| **vLLM** | Draft model, EAGLE, MTP, n-gram, suffix decoding | Most comprehensive open-source support; best at low-medium QPS |
| **TensorRT-LLM** | Draft model, EAGLE-3, recurrent drafting | NVIDIA's optimized inference engine; up to 3.6x throughput |
| **SGLang** | Draft model, EAGLE | High-performance serving framework |
| **Google Search (AI Overviews)** | Speculative decoding | Production deployment at scale |
| **Hugging Face Transformers** | Assisted generation (draft model) | Accessible reference implementation |
| **NVIDIA Model Optimizer** | EAGLE-3 checkpoint generation | Ready-to-deploy speculation modules on HF Hub |
| **P-EAGLE (AWS)** | Parallel EAGLE-3 | Generates all K draft tokens in single forward pass; 1.69x over EAGLE-3 |

## Applications

| Application Domain | How Speculative Decoding Helps |
|--------------------|---------------------------------|
| **Interactive chat / assistants** | Reduces perceived latency; text appears in multi-token chunks |
| **Code generation** | Highly predictable token sequences yield high acceptance rates |
| **Translation & summarization** | Original benchmark domain; 2-3x demonstrated speedup |
| **Batch inference pipelines** | Reduces cost per token for large-scale offline generation |
| **Edge deployment** | Enables larger models on constrained hardware via draft-model pairing |
| **Multimodal generation** | Extended to image generation (arXiv:2410.03355) and speech synthesis (arXiv:2410.21951) |

## Challenges and Limitations

- **Draft model quality dependency**: Speedup degrades significantly when draft model poorly approximates target distribution; requires careful model selection or training
- **Memory overhead**: Maintaining both draft and target models in GPU memory increases VRAM requirements (mitigated by self-speculative and Medusa variants)
- **Batch size limitations**: Speculative decoding is most effective at batch size 1 or small batches; at high concurrency, the increased batch size from speculated tokens creates computational overhead that can negate benefits
- **Decoding strategy constraints**: Currently supports greedy search and sampling; limited compatibility with beam search or diverse sampling strategies
- **Variable latency**: Rejection cascades when draft quality is poor can produce latency spikes; worst-case latency is higher than standard decoding
- **Tokenizer alignment**: Draft and target models must share the same tokenizer/vocabulary for standard approaches (some recent work relaxes this)
- **Training overhead**: Medusa and EAGLE variants require training additional heads, adding development complexity
- **Diminishing returns at scale**: As hardware becomes more compute-bound (e.g., very large batch sizes), the memory-bandwidth assumption weakens

## Related Terms
- **[Transformer](term_transformer.md)**: The foundational architecture that speculative decoding optimizes inference for
- **[LLM](term_llm.md)**: Large Language Models are the primary beneficiaries of speculative decoding
- **[Embedding](term_embedding.md)**: Dense vector representations used in transformer hidden states that EAGLE-style methods draft from
- **[Scaling Law](term_scaling_law.md)**: Governs the relationship between model size and capability; speculative decoding allows using larger models within latency budgets
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation often combines with speculative decoding in production serving stacks
- **[BERT](term_bert.md)**: Encoder-only transformer; contrasts with the decoder-only models that speculative decoding primarily accelerates

## References

### Vault Sources

### External Sources
- [Leviathan, Kalman, Matias (2022). "Fast Inference from Transformers via Speculative Decoding." ICML 2023](https://arxiv.org/abs/2211.17192) -- original speculative decoding paper
- [Chen, Borgeaud, Irving et al. (2023). "Accelerating Large Language Model Decoding with Speculative Sampling." ICML 2023](https://arxiv.org/abs/2302.01318) -- concurrent independent work introducing speculative sampling
- [Xia et al. (2024). "Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding." ACL Findings 2024](https://arxiv.org/abs/2401.07851) -- comprehensive survey of speculative decoding methods
- [Google Research Blog: "Looking Back at Speculative Decoding"](https://research.google/blog/looking-back-at-speculative-decoding/) -- retrospective from the original authors
- [NVIDIA Technical Blog: "An Introduction to Speculative Decoding"](https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/) -- practical guide with TensorRT-LLM integration
- [PyTorch Blog: "A Hitchhiker's Guide to Speculative Decoding"](https://pytorch.org/blog/hitchhikers-guide-speculative-decoding/) -- implementation guide with PyTorch examples
- [vLLM Documentation: Speculative Decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/) -- production serving framework documentation
- [Li et al. (2024). "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty." ICML 2024](https://arxiv.org/abs/2401.15077) -- EAGLE method for feature-level speculative drafting

---

**Last Updated**: March 17, 2026
**Status**: Active - rapidly evolving inference optimization technique
