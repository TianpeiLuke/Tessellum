---
tags:
  - resource
  - terminology
  - deep_learning
  - positional_encoding
keywords:
  - RoPE
  - rotary position embedding
  - rotary positional encoding
  - relative position
  - rotation matrix
  - length generalization
  - context window extension
  - Su et al
topics:
  - Deep Learning
  - Positional Encoding
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Rotary Position Embedding (RoPE)

## Definition

**Rotary Position Embedding (RoPE)** is a positional encoding method that encodes position information by rotating query and key vectors in the attention mechanism using position-dependent rotation matrices. Introduced by Su et al. (2021), RoPE elegantly encodes both absolute and relative position information through a single mechanism: each position applies a different rotation angle, and the dot product between rotated queries and keys naturally produces a function of relative position. Unlike absolute positional embeddings (added once at the input) or relative position bias (added to attention scores), RoPE is applied at every layer to query and key vectors, providing positional information throughout the network. RoPE became the dominant positional encoding after adoption by LLaMA (2023) and is now standard in nearly all modern open-source LLMs.

## Full Name

**RoPE** — Rotary Position Embedding

**Also Known As**: Rotary positional encoding, rotary embeddings, RoPE embeddings

## Mathematical Formulation

### Core Idea

For a query vector $q$ at position $m$ and a key vector $k$ at position $n$, RoPE applies position-dependent rotations:

$$q_m = R_m q, \quad k_n = R_n k$$

where $R_m$ is a rotation matrix parameterized by position $m$.

The attention score becomes:

$$q_m^T k_n = (R_m q)^T (R_n k) = q^T R_m^T R_n k = q^T R_{n-m} k$$

Since $R_m^T R_n = R_{n-m}$ (rotation composition), the dot product is a function of relative position $(n - m)$ — achieving relative positional encoding through absolute rotations.

### Rotation Matrix (2D case)

For each pair of dimensions $(2i, 2i+1)$, apply a 2D rotation:

$$R_m^{(i)} = \begin{pmatrix} \cos(m\theta_i) & -\sin(m\theta_i) \\ \sin(m\theta_i) & \cos(m\theta_i) \end{pmatrix}$$

where $\theta_i = 10000^{-2i/d}$ (following the sinusoidal frequency pattern from Vaswani et al., 2017).

The full rotation is applied block-diagonally across all dimension pairs.

### Frequency Base

The angular frequencies $\theta_i = \text{base}^{-2i/d}$ determine the "wavelengths" at which positions are encoded:
- Low-frequency components (large $i$): capture long-range position relationships
- High-frequency components (small $i$): capture short-range position relationships

Default base: 10,000 (same as original sinusoidal encoding). Extended context methods modify this (e.g., CodeLlama uses base = 1,000,000 for 100K context).

## Comparison with Other Position Methods

| Method | Where Applied | Absolute/Relative | Per-Layer | Length Generalization |
|--------|-------------|-------------------|-----------|---------------------|
| **Sinusoidal** (Vaswani 2017) | Input embeddings | Absolute | No | Poor |
| **Learned absolute** (GPT-2) | Input embeddings | Absolute | No | None (fixed max length) |
| **Relative position bias** (T5) | Attention scores | Relative | Yes (learned per head) | Moderate |
| **ALiBi** (Press 2022) | Attention scores | Relative | Yes (fixed slope) | Good |
| **RoPE** (Su 2021) | Query/Key vectors | Both (absolute rotation → relative dot product) | Yes | Good |

## Key Properties

| Property | Description |
|----------|-------------|
| **Relative position encoding** | Dot product depends only on $n - m$, not absolute positions |
| **Decaying inter-token dependency** | Dot product magnitude decreases with distance (built-in distance decay) |
| **Per-layer application** | Applied at every layer to Q and K, providing positional information throughout |
| **No learned parameters** | Rotation angles are deterministic (from frequency formula) — zero additional parameters |
| **Efficient computation** | Rotation is equivalent to element-wise multiplication of complex numbers |

## Context Window Extension Methods

RoPE's frequency-based design enables context window extension without retraining:

| Method | Approach | Result |
|--------|----------|--------|
| **Position Interpolation** (Chen et al., 2023) | Scale positions to fit original range | Extend context with minimal fine-tuning |
| **NTK-aware scaling** (Reddit, 2023) | Modify the base frequency | Better long-range performance |
| **YaRN** (Peng et al., 2023) | Combine NTK with temperature scaling | State-of-the-art extension |
| **CodeLlama base change** | Use base = 1,000,000 | 100K context from 4K base |

## Adoption in Foundation Models

| Model | Year | Positional Encoding |
|-------|------|-------------------|
| Original Transformer | 2017 | Sinusoidal (fixed) |
| GPT-2/3 | 2019/2020 | Learned absolute |
| T5 | 2020 | Relative position bias |
| GPTNeo | 2021 | RoPE |
| **LLaMA** | **2023** | **RoPE** |
| Llama-2/3, Mistral, Gemma, Qwen, Yi | 2023-2024 | RoPE |

## Applications to Our Work

- **Long-context abuse investigation**: RoPE's length generalization is relevant for processing long buyer interaction histories (multi-turn conversations, extended order histories)
- **Context window extension**: Methods like YaRN enable extending context without retraining — useful for abuse models that need to process long investigation documents

## Related Terms

### Positional Encoding Family
- [Positional Encoding](term_positional_encoding.md) — The broader category; RoPE is a specific implementation
- [Transformer](term_transformer.md) — Architecture where RoPE replaces original sinusoidal encoding
- [Attention Mechanism](term_attention_mechanism.md) — RoPE is applied to Q and K vectors within the attention computation

### Architecture Pattern (LLaMA trio)
- [RMSNorm](term_rmsnorm.md) — First component: pre-normalization
- [SwiGLU](term_swiglu.md) — Second component: FFN activation
- [LLM](term_llm.md) — RoPE is now standard in open-source LLMs

## References

- Su, J. et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding. arXiv:2104.09864.
- Vaswani, A. et al. (2017). [Attention Is All You Need](../papers/lit_vaswani2017attention.md). NeurIPS. arXiv:1706.03762.
- Touvron, H. et al. (2023). [LLaMA: Open and Efficient Foundation Language Models](../papers/lit_touvron2023llama.md). arXiv:2302.13971.
- Chen, S. et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation. arXiv:2306.15595.
- Peng, B. et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv:2309.00071.
- Press, O. et al. (2022). ALiBi: Train Short, Test Long. ICLR. arXiv:2108.12409.
