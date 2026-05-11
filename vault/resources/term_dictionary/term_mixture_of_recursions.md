---
tags:
  - resource
  - terminology
  - llm
  - efficient_inference
  - recursive_transformer
  - adaptive_computation
keywords:
  - Mixture-of-Recursions
  - MoR
  - recursive transformer
  - adaptive computation
  - token-level routing
  - parameter sharing
  - weight tying
  - selective KV caching
  - early exit
topics:
  - Large Language Models
  - Efficient AI
  - Model Architecture
language: markdown
date of note: 2026-03-31
status: active
building_block: concept
---

# Mixture-of-Recursions (MoR)

## Definition

**Mixture-of-Recursions (MoR)** is an efficient language model architecture (Bae et al., 2025) that unifies **parameter sharing** (via weight-tied recursive Transformer layers) with **adaptive token-level computation** (via learned routers that assign different recursion depths to individual tokens). A shared stack of $L$ layers is reused across $R$ recursion steps for an effective depth of $L \times R$, but lightweight routers allow easy tokens to exit after fewer recursions while complex tokens recurse to the full depth. Selective KV caching stores only active tokens' key-value pairs, reducing both compute and memory.

MoR can be understood as **MoE applied to depth instead of parameters**: Mixture-of-Experts routes tokens to different expert networks; Mixture-of-Recursions routes tokens to different computation depths.

## Key Properties

- **Dual efficiency**: Simultaneously reduces parameters (weight sharing across recursion steps) and compute (early token exit via routing)
- **Token-level adaptive depth**: Routers learn which tokens need deep recursion (complex reasoning) vs. shallow (function words, punctuation)
- **Selective KV caching**: Only active tokens' KV pairs are cached at each depth, reducing memory proportionally to early-exit fraction
- **KV sharing variant**: Reuses first-recursion KV pairs across all depths for further memory savings
- **Pareto improvement**: At 135M–1.7B scale, achieves lower perplexity and higher throughput than vanilla Transformers at equal FLOPs
- **Up to 2× throughput**: Compared to standard Transformers at similar accuracy
- **Built on Llama**: Practical implementation modifying LlamaForCausalLM

## Architecture

| Component | Description |
|-----------|-------------|
| **Shared layer stack** | $L$ Transformer layers reused across $R$ recursion steps |
| **Routers** | Lightweight linear classifiers deciding which tokens continue at each depth |
| **Router variants** | Expert-choice (fixed budget per depth) or token-choice (variable budget) |
| **Selective attention** | Quadratic attention only among active tokens at each depth |
| **KV cache** | Only active tokens cached; optional KV sharing from first recursion |

## Related Terms

- **[MoE](term_moe.md)**: Routes tokens across parameter space (experts); MoR routes across depth (recursions) — complementary, potentially combinable
- **[Transformer](term_transformer.md)**: MoR modifies the standard Transformer with weight tying and routing
- **[Scaling Law](term_scaling_law.md)**: MoR challenges the assumption that more parameters = better quality
- **[Phi](term_phi.md)**: Complementary efficiency approach — Phi achieves efficiency via data quality, MoR via architecture
- **[Knowledge Distillation](term_knowledge_distillation.md)**: Alternative efficiency mechanism (model compression) vs. MoR's architectural approach
- **[Foundation Model](term_foundation_model.md)**: MoR aims to achieve foundation model quality with smaller, faster models

## References

### Vault Sources

- [MoR Literature Note](../papers/lit_bae2025mixture.md) — Full paper digest with section notes
- [MoR Review](../papers/review_bae2025mixture.md) — OpenReview-style evaluation (Overall 6/10)

### External Sources

- [Bae et al. (2025). "Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation." arXiv:2507.10524](https://arxiv.org/abs/2507.10524)
- [GitHub: raymin0223/mixture_of_recursions](https://github.com/raymin0223/mixture_of_recursions) — Open-source implementation
- [Dehghani et al. (2019). "Universal Transformers." ICLR](https://arxiv.org/abs/1807.03819) — Predecessor: recursive Transformer with uniform depth
