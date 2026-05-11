---
tags:
  - resource
  - literature_note
  - attention
  - gpu_optimization
  - transformers
  - systems
keywords:
  - FlashAttention
  - IO-aware
  - tiling
  - GPU memory hierarchy
  - HBM
  - SRAM
  - online softmax
  - recomputation
  - block-sparse attention
  - fused CUDA kernel
  - exact attention
  - memory-efficient
topics:
  - Systems for Machine Learning
  - Efficient Transformers
  - GPU Optimization
domain: "Efficient Inference"
language: markdown
date of note: 2026-03-09
paper_title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
authors:
  - Tri Dao
  - Daniel Y. Fu
  - Stefano Ermon
  - Atri Rudra
  - Christopher Ré
year: 2022
source: "arXiv:2205.14135"
venue: "NeurIPS 2022"
DOI: "10.52202/068431-1189"
arXiv: "2205.14135"
semantic_scholar_id: "87c5b281fa43e6f27191b20a8dd694eda1126336"
zotero_key: "9UZXDXZM"
paper_id: dao2022flashattention
paper_notes:
  - paper_dao2022flashattention_intro.md
  - paper_dao2022flashattention_contrib.md
  - paper_dao2022flashattention_algo.md
  - paper_dao2022flashattention_exp_design.md
  - paper_dao2022flashattention_exp_result.md
status: active
building_block: hypothesis
---

# FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness |
| **Authors** | Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré |
| **Year** | 2022 |
| **Venue** | NeurIPS 2022 |
| **arXiv** | [2205.14135](https://arxiv.org/abs/2205.14135) |
| **Semantic Scholar** | [87c5b281fa...](https://www.semanticscholar.org/paper/87c5b281fa43e6f27191b20a8dd694eda1126336) |
| **Zotero** | 9UZXDXZM |
| **Citations** | ~3725 |

## Abstract

Transformers are slow and memory-hungry on long sequences, since the time and memory complexity of self-attention are quadratic in sequence length. Approximate attention methods have attempted to address this problem by trading off model quality to reduce the compute complexity, but often do not achieve wall-clock speedup. We argue that a missing principle is making attention algorithms IO-aware -- accounting for reads and writes between levels of GPU memory. We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM. We analyze the IO complexity of FlashAttention, showing that it requires fewer HBM accesses than standard attention, and is optimal for a range of SRAM sizes. We also extend FlashAttention to block-sparse attention, yielding an approximate attention algorithm that is faster than any existing approximate attention method. FlashAttention trains Transformers faster than existing baselines: 15% end-to-end wall-clock speedup on BERT-large (seq. length 512) compared to the MLPerf 1.1 training speed record, 3x speedup on GPT-2 (seq. length 1K), and 2.4x speedup on long-range arena (seq. length 1K-4K). FlashAttention and block-sparse FlashAttention enable longer context in Transformers, yielding higher quality models (0.7 better perplexity on GPT-2 and 6.4 points of lift on long-document classification) and entirely new capabilities: the first Transformers to achieve better-than-chance performance on the Path-X challenge (seq. length 16K, 61.4% accuracy) and Path-256 (seq. length 64K, 63.1% accuracy).

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_dao2022flashattention_intro](paper_dao2022flashattention_intro.md) | Self-attention is O(N^2) in time and memory; approximate methods trade quality for compute but miss wall-clock speedup because they ignore GPU memory hierarchy IO costs |
| **Contribution** | [paper_dao2022flashattention_contrib](paper_dao2022flashattention_contrib.md) | IO-aware exact attention via tiling; proven optimal HBM access complexity; extension to block-sparse attention; practical speedups across BERT, GPT-2, LRA |
| **Method** | [paper_dao2022flashattention_algo](paper_dao2022flashattention_algo.md) | Block-wise Q/K/V loading from HBM to SRAM; online softmax with running max and sum statistics; recomputation instead of materialization of N x N attention matrix; single fused CUDA kernel |
| **Experiment Design** | [paper_dao2022flashattention_exp_design](paper_dao2022flashattention_exp_design.md) | Benchmarks on BERT-large (MLPerf), GPT-2 (HuggingFace), Long Range Arena (1K-4K), Path-X (16K), Path-256 (64K); runtime and memory comparisons against standard and approximate attention |
| **Experiment Results** | [paper_dao2022flashattention_exp_result](paper_dao2022flashattention_exp_result.md) | 15% speedup on BERT-large over MLPerf record; 3x on GPT-2; 2.4x on LRA; first to solve Path-X (61.4%) and Path-256 (63.1%); up to 20x memory reduction |
| **Review** | [review_dao2022flashattention](review_dao2022flashattention.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (4 review lenses applied) |

## Summary

- **Background**: Self-attention in Transformers has O(N^2) time and memory complexity, making it prohibitively slow and memory-hungry on long sequences. Approximate attention methods attempt to reduce compute complexity by trading off model quality, but often do not achieve wall-clock speedup because they ignore IO costs between GPU memory levels (HBM vs SRAM). The key missing principle is IO-awareness -- accounting for reads and writes between levels of the GPU memory hierarchy. <!-- VERIFY: problem statement -->
- **Contribution**: FlashAttention is an IO-aware exact attention algorithm that uses tiling and recomputation to reduce the number of HBM accesses from Theta(Nd + N^2) (standard attention) to Theta(N^2 d^2 M^{-1}), where N is sequence length, d is head dimension, and M is SRAM size. The authors prove this is optimal for a range of SRAM sizes. The algorithm is extended to block-sparse attention, yielding IO complexity proportional to sparsity ratio, faster than any existing approximate attention method.
- **Method**: The algorithm splits Q, K, V matrices into blocks that fit in SRAM, loads blocks from HBM to SRAM, and computes attention block-by-block using an online softmax algorithm that maintains running max and sum statistics across blocks. Only the output O and softmax normalization statistics are stored for the backward pass; the full N x N attention matrix is never materialized in HBM. Instead, it is recomputed from Q, K, V blocks during backpropagation. The entire forward pass is implemented as a single fused CUDA kernel, eliminating intermediate HBM reads/writes. <!-- VERIFY: method details -->
- **Results**: FlashAttention achieves 15% end-to-end wall-clock speedup on BERT-large (seq. length 512) over the MLPerf 1.1 training speed record; 3x speedup on GPT-2 (seq. length 1K) over HuggingFace baseline; and 2.4x speedup on Long Range Arena (seq. length 1K-4K). It enables 4x longer context with better perplexity (0.7 improvement on GPT-2) and 6.4 points of lift on long-document classification. FlashAttention produces the first Transformer to achieve better-than-chance performance on the Path-X challenge (seq. length 16K, 61.4% accuracy) and Path-256 (seq. length 64K, 63.1% accuracy). Memory usage is reduced by up to 20x, achieving a linear memory footprint in sequence length. <!-- VERIFY: exact numbers -->

## Relevance to Our Work

- **[Self-Attention](../term_dictionary/term_self_attention.md)**: FlashAttention computes exact self-attention with reduced IO complexity, demonstrating that hardware-aware algorithm design can achieve speedups without approximating the attention computation
- **[Transformer](../term_dictionary/term_transformer.md)**: FlashAttention is the core optimization enabling longer-context Transformers, directly impacting model quality and enabling new capabilities on tasks requiring long-range dependencies
- **[Multi-Head Attention](../term_dictionary/term_multi_head_attention.md)**: FlashAttention applies per-head and is fully compatible with multi-head attention architectures, serving as a drop-in replacement for standard attention
- **[Attention Mechanism](../term_dictionary/term_attention_mechanism.md)**: FlashAttention is an implementation optimization of the attention mechanism that preserves mathematical equivalence while fundamentally changing the memory access pattern
- **[Scaling Law](../term_dictionary/term_scaling_law.md)**: IO-awareness changes the compute-memory tradeoff landscape for scaling, as the bottleneck shifts from FLOPs to memory bandwidth at longer sequence lengths
- **[BERT](lit_devlin2019bert.md)**: BERT-large serves as a key benchmark; FlashAttention achieves 15% speedup over the MLPerf 1.1 training speed record
- **[GPT-2](lit_radford2019language.md)**: GPT-2 serves as a key benchmark; FlashAttention achieves 3x training speedup over HuggingFace implementation and enables longer context with better perplexity

## Related Documentation

### Paper Notes
- [Introduction](paper_dao2022flashattention_intro.md)
- [Contribution](paper_dao2022flashattention_contrib.md)
- [Method](paper_dao2022flashattention_algo.md)
- [Experiment Design](paper_dao2022flashattention_exp_design.md)
- [Experiment Results](paper_dao2022flashattention_exp_result.md)

### Related Vault Notes
- [Self-Attention](../term_dictionary/term_self_attention.md) — FlashAttention computes exact self-attention with reduced IO
- [Transformer](../term_dictionary/term_transformer.md) — FlashAttention is the core optimization enabling longer-context Transformers
- [Multi-Head Attention](../term_dictionary/term_multi_head_attention.md) — FlashAttention applies per-head, compatible with multi-head attention
- [Attention Mechanism](../term_dictionary/term_attention_mechanism.md) — FlashAttention is an implementation optimization of the attention mechanism
- [Scaling Law](../term_dictionary/term_scaling_law.md) — IO-awareness changes the compute-memory tradeoff landscape for scaling
- [BERT](lit_devlin2019bert.md) — BERT-large training speedup benchmark (15% over MLPerf record)
- [GPT-2](lit_radford2019language.md) — GPT-2 training speedup benchmark (3x over HuggingFace)

### Related Literature
- Vaswani et al. (2017). "Attention Is All You Need" — [lit_vaswani2017attention](lit_vaswani2017attention.md)
- Devlin et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — [lit_devlin2019bert](lit_devlin2019bert.md)
- Radford et al. (2019). "Language Models are Unsupervised Multitask Learners" — [lit_radford2019language](lit_radford2019language.md)
- Katharopoulos et al. (2020). "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention" — Linear attention baseline
- Choromanski et al. (2021). "Rethinking Attention with Performers" — Performer approximate attention baseline
- Rabe & Staats (2021). "Self-attention Does Not Need O(n^2) Memory" — Memory-efficient attention via chunking
