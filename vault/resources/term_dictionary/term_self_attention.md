---
tags:
  - resource
  - terminology
  - deep_learning
  - transformer
  - attention
keywords:
  - self-attention
  - intra-attention
  - query key value
  - scaled dot-product
  - sequence modeling
  - permutation equivariance
  - bidirectional attention
  - causal attention
topics:
  - Deep Learning
  - Neural Architecture
  - Natural Language Processing
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Self-Attention

## Definition

**Self-Attention** (also called **intra-attention**) is a special case of attention where queries, keys, and values all derive from the same sequence. Each position computes attention weights over all other positions in the same layer, enabling direct information flow between any two positions in O(1) operations. In the Transformer (Vaswani et al., 2017), self-attention is the sole mechanism for computing sequence representations, replacing recurrence and convolution entirely. Unlike RNNs where information between distant positions must traverse O(n) sequential steps, self-attention connects all positions directly, making it both more parallelizable and more effective at capturing long-range dependencies.

## Full Name

**Self-Attention** (Intra-Attention)

**Also Known As**: Intra-attention, within-sequence attention

## Mathematical Formulation

Given an input sequence $X \in \mathbb{R}^{n \times d_{model}}$, self-attention computes:

$$Q = XW^Q, \quad K = XW^K, \quad V = XW^V$$

$$\text{SelfAttention}(X) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

where $W^Q, W^K \in \mathbb{R}^{d_{model} \times d_k}$ and $W^V \in \mathbb{R}^{d_{model} \times d_v}$ are learned projection matrices.

**Key property**: Q, K, V all come from the same input $X$. This distinguishes self-attention from **cross-attention**, where Q comes from one sequence and K, V from another.

**Permutation equivariance**: Without positional encoding, self-attention is permutation-equivariant — permuting the input permutes the output identically. This is why positional encoding is required to inject sequence order information.

## Variants

| Variant | Masking | Directionality | Use Case |
|---------|---------|---------------|----------|
| **Bidirectional** | None | Each position attends to all positions | BERT encoder: full context for classification/NLU |
| **Causal (masked)** | Upper-triangular $-\infty$ mask | Each position attends only to preceding positions | GPT/LLaMA decoder: autoregressive generation |
| **Local/windowed** | Window mask of size $w$ | Each position attends to $w$ nearest positions | Longformer: efficient processing of long documents |

**Causal masking** sets attention scores to $-\infty$ for positions $j > i$ before softmax, ensuring the model cannot "peek" at future tokens during autoregressive generation. This is essential for all decoder-only LLMs (GPT, Claude, LLaMA).

## Why Self-Attention Works

### Computational Advantages Over Recurrence

| Property | Self-Attention | RNN/LSTM |
|----------|---------------|----------|
| Maximum path length | O(1) | O(n) |
| Sequential operations per layer | O(1) | O(n) |
| Complexity per layer | O(n²·d) | O(n·d²) |
| Parallelizable | Fully | Not within sequence |

Self-attention dominates when $n < d$ (typical for NLP: $n \leq 512$, $d = 768$). For very long sequences ($n \gg d$), the O(n²) cost becomes a bottleneck — motivating efficient attention variants.

### What Self-Attention Learns

Empirical analysis of Transformer attention heads (Vaswani et al., 2017; Clark et al., 2019) shows heads specialize in:
- **Syntactic dependencies**: Subject-verb agreement across clauses
- **Positional proximity**: Attending to adjacent or nearby tokens
- **Coreference**: Linking pronouns to their antecedents
- **Semantic similarity**: Grouping semantically related tokens

This emergent specialization occurs without explicit supervision — the model discovers these patterns through gradient descent alone.

## Complexity Analysis

| Component | Time | Space | Note |
|-----------|------|-------|------|
| Attention matrix computation ($QK^T$) | $O(n^2 d_k)$ | $O(n^2)$ | The quadratic bottleneck |
| Attention-weighted values ($\text{softmax} \cdot V$) | $O(n^2 d_v)$ | $O(n \cdot d_v)$ | |
| Total per layer | $O(n^2 d)$ | $O(n^2 + nd)$ | Quadratic in sequence length |

For BERT-BASE ($n=512$, $d=768$): attention matrix = 262K entries — manageable. For long-context LLMs ($n=128K$): 16.4B entries — requires Flash Attention or sparse methods.

## Ablation Evidence

From the Transformer paper ablation study (Table 3):
- Self-attention with single head ($h=1$): 24.9 BLEU (-0.9 vs. baseline 25.8)
- Multi-head self-attention ($h=8$): 25.8 BLEU (optimal)
- Too many heads ($h=32$, $d_k=16$): 25.4 BLEU (-0.4)

The single-head result confirms that multi-head decomposition is critical — a single attention function, by averaging attention patterns, inhibits the model's ability to focus on different relational patterns simultaneously.

## Applications to Our Work

- **BERT-based abuse classifiers** ([RnR BSM BERT](../../areas/models/model_rnr_bsm_bert.md), [AtoZ BSM BERT](../../areas/models/model_atoz_bsm_bert.md)): Bidirectional self-attention enables each token in a buyer-seller message to attend to all other tokens for context-dependent abuse classification
- **[TSA](term_tsa.md)** (Temporal Self-Attention): Self-attention applied over buyer transaction sequences to detect temporal abuse patterns — each transaction attends to all prior transactions
- **[CrossBERT](term_crossbert.md)**: Self-attention within buyer and seller representations, combined with cross-attention between them
- **Graph Transformers** (HGT, TGN): Self-attention adapted for graph neighborhoods — node-level attention over typed edges

## Related Terms

### Core Architecture
- [Attention Mechanism](term_attention_mechanism.md) — Self-attention is a specific case where Q=K=V source is the same sequence
- [Multi-Head Attention](term_multi_head_attention.md) — Self-attention is typically applied in multi-head form
- [Transformer](term_transformer.md) — Architecture built entirely on self-attention
- [Positional Encoding](term_positional_encoding.md) — Required because self-attention is permutation-equivariant

### Models Using Self-Attention
- [BERT](term_bert.md) — Bidirectional self-attention encoder
- [LLM](term_llm.md) — Causal self-attention decoder
- [TSA](term_tsa.md) — Temporal self-attention for abuse patterns
- [CrossBERT](term_crossbert.md) — Self-attention + cross-attention for buyer-seller interactions

## References

- Vaswani, A. et al. (2017). [Attention Is All You Need](../papers/lit_vaswani2017attention.md). NeurIPS. arXiv:1706.03762.
- Clark, K. et al. (2019). What Does BERT Look At? An Analysis of BERT's Attention. ACL Workshop on BlackboxNLP. arXiv:1906.04341.
- Shaw, P. et al. (2018). Self-Attention with Relative Position Representations. NAACL. arXiv:1803.02155.
