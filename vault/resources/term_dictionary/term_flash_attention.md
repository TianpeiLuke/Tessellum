---
tags:
  - resource
  - terminology
  - systems_optimization
  - attention
  - gpu_optimization
  - transformer
keywords:
  - flash attention
  - io-aware attention
  - tiling
  - online softmax
  - recomputation
  - fused kernel
  - HBM
  - SRAM
  - memory-efficient attention
  - block-sparse attention
topics:
  - Deep Learning
  - Systems Optimization
  - GPU Computing
  - Transformer Architecture
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
---

# Term: FlashAttention

## Definition

**FlashAttention** is an IO-aware exact attention algorithm (Dao et al., 2022) that computes standard self-attention without any approximation while dramatically reducing GPU high-bandwidth memory (HBM) accesses. Instead of materializing the full $N \times N$ attention matrix in HBM, FlashAttention uses **tiling** to decompose the computation into blocks that fit in fast on-chip SRAM, **online softmax** to compute exact softmax incrementally across blocks, and **recomputation** in the backward pass to avoid storing the large intermediate attention matrix. The result is an algorithm with $\Theta(N^2 d^2 M^{-1})$ HBM accesses instead of the standard $\Theta(Nd + N^2)$, where $M$ is SRAM size, $N$ is sequence length, and $d$ is head dimension. This achieves 2-4x wall-clock speedup over standard attention while using only $O(N)$ memory instead of $O(N^2)$.

## Full Name

**FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness**

**Also Known As**: Flash Attention, IO-aware attention, tiled attention

## Mathematical Formulation

Standard self-attention computes:

$$S = QK^T \in \mathbb{R}^{N \times N}, \quad P = \text{softmax}(S) \in \mathbb{R}^{N \times N}, \quad O = PV \in \mathbb{R}^{N \times d}$$

where $Q, K, V \in \mathbb{R}^{N \times d}$ are the query, key, and value matrices.

**Standard implementation** materializes $S$ and $P$ in HBM, requiring $O(N^2)$ memory and $O(Nd + N^2)$ HBM accesses.

**FlashAttention** computes the same result without ever materializing the full $S$ or $P$ matrices. For block sizes $B_c = \lceil M / 4d \rceil$ and $B_r = \min(\lceil M / 4d \rceil, d)$:

1. **Outer loop**: Load blocks $K_j, V_j \in \mathbb{R}^{B_c \times d}$ from HBM to SRAM
2. **Inner loop**: For each $Q_i \in \mathbb{R}^{B_r \times d}$, compute local attention block $S_{ij} = Q_i K_j^T$
3. **Online softmax update**: Maintain running statistics $m_i$ (row-wise max) and $\ell_i$ (row-wise sum of exponentials) to compute exact softmax incrementally
4. **Accumulate output**: Update $O_i$ with rescaled contribution from current block
5. **Write back**: Store only $O_i, \ell_i, m_i$ to HBM (not $S$ or $P$)

## IO Complexity Analysis

| Algorithm | HBM Accesses | Memory | Exact? |
|-----------|-------------|--------|--------|
| Standard attention | $\Theta(Nd + N^2)$ | $O(N^2)$ | Yes |
| FlashAttention | $\Theta(N^2 d^2 M^{-1})$ | $O(N)$ | Yes |
| Sparse attention (top-k) | $\Theta(Nd + Nk)$ | $O(Nk)$ | No |

**Proposition 3 (Lower bound)**: Any exact attention algorithm requires $\Omega(N^2 d^2 M^{-1})$ HBM accesses, proving FlashAttention is asymptotically optimal.

Since $d \ll M$ (typical: $d = 64\text{-}128$, $M = 20\text{MB} \approx 5\text{M floats}$), FlashAttention requires significantly fewer HBM accesses. For $N = 1024$, $d = 64$: standard requires ~4.2 MB HBM traffic for the attention matrix alone; FlashAttention reduces this proportionally to $d^2 / M$.

## How It Works

### Tiling Strategy

FlashAttention partitions Q, K, V into blocks along the sequence dimension:

- $K$ and $V$ are divided into $T_c = \lceil N / B_c \rceil$ blocks
- $Q$ is divided into $T_r = \lceil N / B_r \rceil$ blocks
- Block sizes are chosen so that all required data fits in SRAM simultaneously: $B_c \cdot d + B_r \cdot d + B_r \cdot B_c \leq M$

### Online Softmax for Incremental Computation

The key challenge is that softmax requires the full row of $S$ to compute the normalizing denominator. FlashAttention uses [online softmax](term_online_softmax.md) to handle this:

For each new block $j$, update:
$$m_i^{(j)} = \max(m_i^{(j-1)}, \text{rowmax}(S_{ij}))$$
$$\ell_i^{(j)} = e^{m_i^{(j-1)} - m_i^{(j)}} \cdot \ell_i^{(j-1)} + \text{rowsum}(e^{S_{ij} - m_i^{(j)}})$$
$$O_i^{(j)} = \text{diag}(e^{m_i^{(j-1)} - m_i^{(j)}}) \cdot O_i^{(j-1)} + e^{S_{ij} - m_i^{(j)}} \cdot V_j$$

After processing all blocks, $O_i = \text{diag}(\ell_i)^{-1} \cdot O_i^{(\text{final})}$ gives the exact attention output.

### Recomputation in Backward Pass

Standard attention stores $S, P \in \mathbb{R}^{N \times N}$ for the backward pass, consuming $O(N^2)$ memory. FlashAttention instead stores only $O, \ell, m$ and **recomputes** $S$ and $P$ block-by-block during backpropagation using the same tiling strategy. This trades extra FLOPs (~33% more) for dramatically less memory, which is a net win because attention is memory-bound, not compute-bound.

### Fused CUDA Kernel

All operations — matrix multiply ($QK^T$), scaling, masking, softmax, dropout, matrix multiply ($PV$) — are fused into a **single GPU kernel**. This eliminates intermediate HBM reads/writes that would occur if each operation were a separate kernel launch.

## Versions

| Version | Year | Key Improvements |
|---------|------|-----------------|
| FlashAttention | 2022 | Original IO-aware tiled algorithm; 2-4x speedup |
| FlashAttention-2 | 2023 | Better work partitioning across thread blocks and warps; reduced non-matmul FLOPs; ~2x faster than v1; reaches 50-73% of theoretical peak FLOPS on A100 |
| FlashAttention-3 | 2024 | Optimized for H100 (Hopper architecture); FP8 support; asynchronous data movement via TMA; warp-specialized pipeline; 1.5-2x faster than FlashAttention-2 on H100 |

### Block-Sparse Extension

FlashAttention natively supports block-sparse attention patterns by skipping blocks where the sparsity mask is entirely zero. This yields IO complexity of $O(N^2 d^2 M^{-1} \cdot s)$ where $s$ is the fraction of non-zero blocks, enabling efficient computation of patterns like local windows, strided attention, and fixed patterns.

## Concrete Performance Numbers

From Dao et al. (2022), on A100 GPU with $N = 1024$, $d = 64$:

| Metric | Standard Attention | FlashAttention |
|--------|-------------------|----------------|
| HBM accesses | 40.3 GB | 4.4 GB |
| GFLOPs | 66.6 | 75.2 |
| Wall-clock time | Baseline | 7.6x faster |

FlashAttention performs **more** FLOPs (due to recomputation) but is **faster** because it is no longer bottlenecked by HBM bandwidth. This demonstrates the core [IO-awareness](term_io_awareness.md) insight.

## Adoption and Impact

- **PyTorch 2.0+**: Integrated as `torch.nn.functional.scaled_dot_product_attention` with automatic dispatch to FlashAttention kernels
- **Hugging Face Transformers**: Default attention backend for supported models
- **vLLM**: Used in high-throughput LLM serving
- **Context length scaling**: Enables practical training with 4K-64K+ context lengths; instrumental in GPT-4, Claude, and LLaMA long-context variants
- **Citations**: 3725+ (as of 2024), one of the most impactful systems papers in modern deep learning

## Applications to Our Work

- **Long buyer-seller message sequences**: FlashAttention enables our BERT-based classifiers ([RnR BSM BERT](../../areas/models/model_rnr_bsm_bert.md), [AtoZ BSM BERT](../../areas/models/model_atoz_bsm_bert.md)) to process longer conversation threads without memory blowup
- **Temporal Self-Attention ([TSA](term_tsa.md))**: Buyer transaction sequences can scale to longer histories with FlashAttention as the attention backend
- **Inference serving**: [vLLM](term_vllm.md) uses FlashAttention for efficient LLM inference in abuse detection pipelines
- **Training efficiency**: Enables faster iteration when fine-tuning Transformer models on abuse datasets

## Related Terms

### Core Concepts
- [Self-Attention](term_self_attention.md) — The operation that FlashAttention computes exactly but more efficiently
- [Multi-Head Attention](term_multi_head_attention.md) — FlashAttention applies independently to each head
- [Transformer](term_transformer.md) — Architecture whose bottleneck FlashAttention addresses
- [Attention Mechanism](term_attention_mechanism.md) — General attention framework

### Systems Techniques
- [IO-Awareness](term_io_awareness.md) — Design principle underlying FlashAttention
- [Tiling](term_tiling.md) — Block decomposition strategy used for Q, K, V processing
- [Online Softmax](term_online_softmax.md) — Incremental softmax algorithm enabling tiled computation
- [Kernel Fusion](term_kernel_fusion.md) — All attention operations fused into a single GPU kernel

### Related Systems
- [KV Cache](term_kv_cache.md) — Complementary optimization for autoregressive inference
- [vLLM](term_vllm.md) — Inference engine using FlashAttention
- **[Gist Token](term_gist_token.md)**: Complementary optimization — FlashAttention reduces IO cost of attention computation while gist tokens reduce the number of tokens that need attending

## References

- Dao, T. et al. (2022). [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../papers/lit_dao2022flashattention.md). NeurIPS. arXiv:2205.14135.
- Dao, T. (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. arXiv:2307.08691.
- Shah, J. et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision. arXiv:2407.08691.
- Milakov, M. & Gimelshein, N. (2018). Online Normalizer Calculation for Softmax. arXiv:1805.02867.
- Rabe, M.N. & Staats, C. (2022). Self-Attention Does Not Need O(n²) Memory. arXiv:2112.05682.
