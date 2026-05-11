---
tags:
  - resource
  - terminology
  - deep_learning
  - activation_function
keywords:
  - SwiGLU
  - activation function
  - gated linear unit
  - GLU
  - Swish
  - feed-forward network
  - transformer FFN
  - PaLM
  - LLaMA
topics:
  - Deep Learning
  - Activation Functions
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: SwiGLU Activation Function

## Definition

**SwiGLU** is a gated activation function combining the Swish activation with a Gated Linear Unit (GLU) mechanism. Introduced by Shazeer (2020), SwiGLU replaces the standard ReLU or GELU activation in the Transformer feed-forward network (FFN) with a gated variant that consistently improves performance across model scales and tasks. SwiGLU uses two linear projections — one passed through Swish and one kept linear — which are multiplied element-wise to produce the output. Adopted by PaLM (2022) and LLaMA (2023), SwiGLU has become the default activation function in modern open-source LLMs.

## Full Name

**SwiGLU** — Swish-Gated Linear Unit

**Also Known As**: Gated activation, GLU variant

## Mathematical Formulation

### Standard Transformer FFN (ReLU)

$$\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$$

Two linear projections with ReLU non-linearity. Parameters: $W_1 \in \mathbb{R}^{d \times 4d}$, $W_2 \in \mathbb{R}^{4d \times d}$.

### GLU (Gated Linear Unit, Dauphin et al., 2017)

$$\text{GLU}(x, W, V) = (xW) \otimes \sigma(xV)$$

where $\sigma$ is the sigmoid function and $\otimes$ is element-wise multiplication. One branch is gated by the sigmoid of the other.

### SwiGLU

$$\text{SwiGLU}(x, W, V, b, c) = \text{Swish}(xW + b) \otimes (xV + c)$$

where $\text{Swish}(x) = x \cdot \sigma(x)$ (Ramachandran et al., 2017).

### LLaMA's FFN with SwiGLU

LLaMA uses SwiGLU with a reduced hidden dimension of $\frac{2}{3} \cdot 4d$ (instead of $4d$) to maintain the same parameter count:

$$\text{FFN}_{\text{SwiGLU}}(x) = \left(\text{Swish}(xW_{\text{gate}}) \otimes xW_{\text{up}}\right) W_{\text{down}}$$

where $W_{\text{gate}}, W_{\text{up}} \in \mathbb{R}^{d \times \frac{8d}{3}}$ and $W_{\text{down}} \in \mathbb{R}^{\frac{8d}{3} \times d}$.

## GLU Variant Comparison

Shazeer (2020) systematically compared 8 GLU variants:

| Variant | Gate Function | Performance Rank |
|---------|--------------|:----------------:|
| **SwiGLU** | Swish (x · σ(x)) | 1st (best) |
| **GEGLU** | GELU | 2nd |
| **ReGLU** | ReLU | 3rd |
| GLU | Sigmoid | 4th |
| Bilinear | Identity | 5th |
| Standard ReLU FFN | — (no gate) | Baseline |
| Standard GELU FFN | — (no gate) | Baseline |

SwiGLU and GEGLU consistently outperform standard FFN across 12 tasks.

## Why SwiGLU Works

1. **Gating mechanism**: The element-wise multiplication allows the network to selectively pass information, functioning as a soft attention over the hidden dimension
2. **Smooth non-linearity**: Swish ($x \cdot \sigma(x)$) is smooth and non-monotonic, unlike ReLU which has a hard zero boundary
3. **Expressiveness**: Two projections ($W_{\text{gate}}$ and $W_{\text{up}}$) with multiplicative interaction create a richer function space than a single projection with point-wise activation

## Parameter Count Adjustment

SwiGLU requires 3 weight matrices (gate, up, down) instead of 2 (up, down) for standard FFN. To maintain the same parameter count, the hidden dimension is reduced from $4d$ to $\frac{8d}{3}$:

| FFN Type | Matrices | Hidden Dim | Params per Layer |
|----------|----------|-----------|:----------------:|
| Standard (ReLU/GELU) | 2 ($W_1, W_2$) | $4d$ | $8d^2$ |
| SwiGLU | 3 ($W_g, W_u, W_d$) | $\frac{8d}{3}$ | $\frac{8d^2}{1} \approx 8d^2$ |

## Adoption in Foundation Models

| Model | Year | Activation | Hidden Dim |
|-------|------|-----------|-----------|
| Original Transformer | 2017 | ReLU | $4d$ |
| GPT-2/3 | 2019/2020 | GELU | $4d$ |
| PaLM | 2022 | SwiGLU | $4d$ |
| **LLaMA** | **2023** | **SwiGLU** | **$\frac{8d}{3}$** |
| Llama-2/3, Mistral, Gemma, Qwen | 2023-2024 | SwiGLU | $\frac{8d}{3}$ |

## Applications to Our Work

- **Model architecture selection**: When fine-tuning or building abuse detection models, SwiGLU-based architectures (LLaMA family) provide better performance than GELU-based alternatives at equivalent parameter counts

## Related Terms

### Activation Functions
- [Transformer](term_transformer.md) — Architecture where SwiGLU replaces standard FFN activation
- [LLM](term_llm.md) — SwiGLU is now standard in open-source LLMs

### Architecture Components
- [RMSNorm](term_rmsnorm.md) — Often paired with SwiGLU in modern architectures (LLaMA pattern)
- [RoPE](term_rope.md) — Third component of the LLaMA architecture pattern (RMSNorm + SwiGLU + RoPE)
- [Attention Mechanism](term_attention_mechanism.md) — SwiGLU is used in the FFN, not the attention mechanism

## References

- Shazeer, N. (2020). GLU Variants Improve Transformer. arXiv:2002.05202.
- Dauphin, Y. et al. (2017). Language Modeling with Gated Convolutional Networks. ICML.
- Ramachandran, P. et al. (2017). Searching for Activation Functions. arXiv:1710.05941.
- Touvron, H. et al. (2023). [LLaMA: Open and Efficient Foundation Language Models](../papers/lit_touvron2023llama.md). arXiv:2302.13971.
- Chowdhery, A. et al. (2022). PaLM: Scaling Language Modeling with Pathways. arXiv:2204.02311.
