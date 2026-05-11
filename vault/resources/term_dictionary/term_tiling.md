---
tags:
  - resource
  - terminology
  - systems_optimization
  - gpu_optimization
  - algorithm_design
keywords:
  - tiling
  - block decomposition
  - loop tiling
  - cache blocking
  - SRAM utilization
  - memory hierarchy
  - data reuse
  - tile size
topics:
  - Systems Optimization
  - GPU Computing
  - Algorithm Design
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
---

# Term: Tiling

## Definition

**Tiling** (also called **loop tiling** or **cache blocking**) is an algorithm design technique that decomposes a large computation into smaller blocks (tiles) sized to fit in fast on-chip memory (SRAM, L1/L2 cache), maximizing data reuse within fast memory and minimizing slower off-chip memory (HBM, DRAM) accesses. In the context of GPU computing and [FlashAttention](term_flash_attention.md), tiling partitions the Q, K, V matrices along the sequence dimension into blocks that can be loaded into GPU SRAM, processed, and written back, so that the full $N \times N$ attention matrix never materializes in HBM.

## Full Name

**Tiling** (Loop Tiling / Cache Blocking / Block Decomposition)

**Also Known As**: Cache blocking, loop blocking, strip mining, tile-based computation

## How Tiling Works

### General Principle

Consider a computation that operates on data of size $D$ bytes, where $D \gg M$ (fast memory capacity). Without tiling, every access goes to slow memory. With tiling:

1. **Partition** the data into blocks of size $B \leq M$
2. **Load** one block into fast memory
3. **Compute** all operations that touch only this block
4. **Write back** results to slow memory
5. **Repeat** for remaining blocks

The speedup comes from **data reuse**: each element loaded into fast memory is used multiple times before being evicted, amortizing the slow memory access cost.

### Classic Example: Matrix Multiplication

For $C = AB$ where $A, B, C \in \mathbb{R}^{N \times N}$:

**Naive**: Each element of $A$ and $B$ is loaded $N$ times from slow memory. Total memory accesses: $O(N^3)$.

**Tiled (block size $B$)**: Partition into $B \times B$ blocks. Load $A_{ij}$ and $B_{jk}$ blocks, compute partial $C_{ik} += A_{ij} B_{jk}$. Each element loaded $N/B$ times. Total memory accesses: $O(N^3 / B)$.

With $B = \sqrt{M}$: memory accesses = $O(N^3 / \sqrt{M})$, which is provably optimal.

### Tiling in FlashAttention

FlashAttention tiles along the sequence dimension:

| Matrix | Tile Size | Number of Tiles |
|--------|-----------|-----------------|
| $K, V$ | $B_c \times d$ where $B_c = \lceil M/4d \rceil$ | $T_c = \lceil N/B_c \rceil$ |
| $Q$ | $B_r \times d$ where $B_r = \min(\lceil M/4d \rceil, d)$ | $T_r = \lceil N/B_r \rceil$ |

**SRAM budget constraint**: The tiles of $Q_i$, $K_j$, $V_j$, the partial attention block $S_{ij}$, and running statistics must all fit simultaneously:

$$B_r \cdot d + B_c \cdot d + B_r \cdot B_c + B_r \cdot 3 \leq M$$

The $B_r \cdot 3$ accounts for the per-row statistics $m_i$, $\ell_i$, and partial output accumulator.

### Tile Size Selection

Optimal tile size balances three constraints:

1. **SRAM capacity**: All working data must fit — larger tiles waste space
2. **Parallelism**: Tiles map to GPU thread blocks; too few tiles underutilize SMs
3. **Arithmetic intensity**: Larger tiles increase data reuse, improving the compute-to-memory ratio

For FlashAttention on A100 (192 KB SRAM per SM, $d = 64$):
- $B_c = B_r = 128$ gives tiles of 128 × 64 = 8192 elements = 32 KB each
- Three matrices (Q, K, V tiles) + attention block + stats ≈ 160 KB, fitting within SRAM

## Performance Impact

From Dao et al. (2022), tiling reduces HBM accesses from $\Theta(Nd + N^2)$ to $\Theta(N^2 d^2 M^{-1})$:

| $N$ | Standard HBM Accesses | Tiled HBM Accesses | Reduction Factor |
|-----|----------------------|--------------------|-----------------:|
| 512 | ~2.1 MB | ~0.4 MB | 5.2× |
| 1024 | ~8.4 MB | ~1.7 MB | 4.9× |
| 4096 | ~134 MB | ~27 MB | 5.0× |
| 16384 | ~2.1 GB | ~430 MB | 5.0× |

The reduction factor scales as $M / d^2$ — larger SRAM or smaller head dimension gives greater benefit.

## Related Concepts

### Multi-Level Tiling

Modern GPUs have multiple memory levels, and optimal algorithms tile at each level:

1. **HBM → L2 cache** (thread block level): ~40 MB L2 on A100
2. **L2 → Shared memory/L1** (warp level): ~192 KB per SM
3. **Shared memory → Registers** (thread level): ~256 KB register file per SM

FlashAttention-2 and -3 add warp-level tiling to improve utilization within each thread block.

### Tiling vs. Approximation

A key insight from FlashAttention: tiling computes the **exact same result** as the untiled algorithm — it is purely a scheduling optimization, not an approximation. This contrasts with approximate attention methods (Performer, Linformer) that change the mathematical operation to reduce complexity.

## Applications to Our Work

- **Attention optimization**: Tiling is automatically applied when using FlashAttention in PyTorch for our Transformer-based models
- **Custom CUDA kernels**: Understanding tiling principles helps when writing or tuning kernels for specialized abuse detection computations
- **Batch processing**: Tiling concepts apply to batching database queries and ETL operations — processing data in chunks that fit in memory

## Related Terms

- [FlashAttention](term_flash_attention.md) — Primary application of tiling to attention computation
- [IO-Awareness](term_io_awareness.md) — Design principle that motivates tiling
- [Online Softmax](term_online_softmax.md) — Enables tiled softmax computation
- [Kernel Fusion](term_kernel_fusion.md) — Complementary optimization often combined with tiling
- [Self-Attention](term_self_attention.md) — The operation being tiled in FlashAttention

## References

- Dao, T. et al. (2022). [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../papers/lit_dao2022flashattention.md). NeurIPS.
- Lam, M., Rothberg, E. & Wolf, M. (1991). The Cache Performance and Optimizations of Blocked Algorithms. ASPLOS.
- Goto, K. & Van De Geijn, R. (2008). Anatomy of High-Performance Matrix Multiplication. ACM TOMS.
