---
tags:
  - resource
  - terminology
  - systems_optimization
  - numerical_computing
  - attention
keywords:
  - online softmax
  - numerically stable softmax
  - running max
  - running sum
  - incremental normalization
  - log-sum-exp trick
  - softmax tiling
topics:
  - Numerical Computing
  - Systems Optimization
  - Deep Learning
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
---

# Term: Online Softmax

## Definition

**Online softmax** is an algorithm that computes the exact softmax function incrementally over a sequence of values without requiring a full pass to determine the global maximum or normalization constant. It maintains running statistics — a running maximum $m$ and a running sum of exponentials $\ell$ — that are updated as each new element (or block of elements) is processed. This enables softmax computation in a single pass through the data, which is critical for [tiled](term_tiling.md) attention algorithms like [FlashAttention](term_flash_attention.md) where the full row of attention scores is never simultaneously available in fast memory.

## Full Name

**Online Softmax** (Single-Pass Numerically Stable Softmax / Incremental Softmax)

**Also Known As**: Streaming softmax, online normalizer calculation, incremental log-sum-exp

## The Problem: Why Standard Softmax Requires Two Passes

The standard softmax of a vector $x \in \mathbb{R}^N$ is:

$$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{N} e^{x_j}}$$

The numerically stable version (to avoid overflow) requires:

1. **Pass 1**: Find $m = \max_j x_j$ (requires seeing all elements)
2. **Pass 2**: Compute $\text{softmax}(x_i) = \frac{e^{x_i - m}}{\sum_j e^{x_j - m}}$ (requires the global max from Pass 1)

This two-pass requirement means the entire vector must be accessible, which is incompatible with tiled computation where only a block of the vector is in fast memory at any time.

## The Online Softmax Algorithm

### Single-Element Update

Process elements $x_1, x_2, \ldots, x_N$ one at a time, maintaining:
- $m^{(k)}$: running maximum after seeing $x_1, \ldots, x_k$
- $\ell^{(k)}$: running sum of adjusted exponentials after seeing $x_1, \ldots, x_k$

**Initialization**: $m^{(0)} = -\infty$, $\ell^{(0)} = 0$

**Update rule** (for each new element $x_k$):
$$m^{(k)} = \max(m^{(k-1)}, x_k)$$
$$\ell^{(k)} = e^{m^{(k-1)} - m^{(k)}} \cdot \ell^{(k-1)} + e^{x_k - m^{(k)}}$$

**Final result**: $\text{softmax}(x_i) = \frac{e^{x_i - m^{(N)}}}{\ell^{(N)}}$

The rescaling factor $e^{m^{(k-1)} - m^{(k)}}$ corrects previous contributions when a new maximum is discovered.

### Block-Wise Update (FlashAttention)

In [FlashAttention](term_flash_attention.md), online softmax operates on blocks rather than individual elements. Given attention scores $S_{ij} = Q_i K_j^T \in \mathbb{R}^{B_r \times B_c}$ for block $j$:

**Update rules** (row-wise, for each block $j$):
$$m_i^{(j)} = \max(m_i^{(j-1)}, \text{rowmax}(S_{ij}))$$
$$\ell_i^{(j)} = e^{m_i^{(j-1)} - m_i^{(j)}} \cdot \ell_i^{(j-1)} + \text{rowsum}(e^{S_{ij} - m_i^{(j)}})$$

**Output accumulation** (the key innovation):
$$O_i^{(j)} = \text{diag}\left(e^{m_i^{(j-1)} - m_i^{(j)}}\right) \cdot O_i^{(j-1)} + e^{S_{ij} - m_i^{(j)}} \cdot V_j$$

**Final normalization**:
$$O_i = \text{diag}(\ell_i^{(\text{final})})^{-1} \cdot O_i^{(\text{final})}$$

The output $O_i$ is the **exact same** result as standard attention — no approximation is introduced.

## Why This Matters

### Enabling Tiled Attention

Without online softmax, tiled attention would require:
1. First pass through all K blocks: compute all $S_{ij}$ blocks and find global row maxima → $O(N^2)$ HBM storage for $S$
2. Second pass: apply softmax using global maxima → another $O(N^2)$ HBM read
3. Third pass: multiply by V → yet another $O(N^2)$ HBM read

Online softmax collapses this into a **single pass**: each K,V block is loaded once, the local attention scores are computed, and the output is accumulated — all in SRAM.

### Numerical Stability

Online softmax is inherently numerically stable because:
- The running maximum $m$ prevents overflow in $e^{x_i - m}$
- The rescaling factor $e^{m^{(k-1)} - m^{(k)}} \leq 1$ (since $m$ only increases), preventing accumulation errors
- The final result is mathematically equivalent to the standard two-pass numerically stable softmax

## Correctness Proof Sketch

**Claim**: After processing all $T$ blocks, $O_i^{(T)} / \ell_i^{(T)} = \text{softmax}(S_i) \cdot V$

**Proof**: By induction on the number of blocks. The rescaling factors ensure that contributions from earlier blocks are properly normalized relative to the global maximum discovered in later blocks. The key identity is:

$$\sum_{j=1}^{T} e^{\text{rowmax}(S_{ij}) - m_i^{(T)}} \cdot \text{rowsum}(e^{S_{ij} - \text{rowmax}(S_{ij})}) = \sum_{j=1}^{N} e^{S_{ij} - m_i^{(T)}} = \ell_i^{(T)}$$

This is Theorem 1 in Dao et al. (2022).

## Historical Context

- **Milakov & Gimelshein (2018)** first described the online normalizer calculation for softmax in the context of efficient GPU implementation
- **Rabe & Staats (2021)** used a similar technique to show that self-attention does not need $O(n^2)$ memory
- **Dao et al. (2022)** combined online softmax with tiling, recomputation, and kernel fusion to create FlashAttention

## Related Terms

- [FlashAttention](term_flash_attention.md) — Primary application; uses online softmax for tiled exact attention
- [Tiling](term_tiling.md) — Block decomposition that online softmax enables
- [IO-Awareness](term_io_awareness.md) — Design principle motivating single-pass algorithms
- [Kernel Fusion](term_kernel_fusion.md) — Online softmax is fused into the FlashAttention kernel
- [Self-Attention](term_self_attention.md) — The operation whose softmax step is computed online
- [Layer Normalization](term_layer_normalization.md) — Another normalization operation with similar online computation considerations

## References

- Dao, T. et al. (2022). [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../papers/lit_dao2022flashattention.md). NeurIPS.
- Milakov, M. & Gimelshein, N. (2018). Online Normalizer Calculation for Softmax. arXiv:1805.02867.
- Rabe, M.N. & Staats, C. (2022). Self-Attention Does Not Need O(n²) Memory. arXiv:2112.05682.
