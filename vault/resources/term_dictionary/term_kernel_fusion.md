---
tags:
  - resource
  - terminology
  - systems_optimization
  - gpu_optimization
  - cuda
keywords:
  - kernel fusion
  - fused kernel
  - operator fusion
  - GPU kernel
  - CUDA kernel
  - memory bandwidth
  - kernel launch overhead
  - intermediate buffers
topics:
  - Systems Optimization
  - GPU Computing
  - Compiler Optimization
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
---

# Term: Kernel Fusion

## Definition

**Kernel fusion** (also called **operator fusion**) is a GPU optimization technique that combines multiple sequential operations into a single GPU kernel launch, eliminating intermediate memory reads/writes to HBM between operations. Instead of launching separate kernels that each read inputs from HBM, compute, and write outputs back to HBM, a fused kernel keeps intermediate results in fast on-chip memory (registers and SRAM) throughout the entire computation chain. This reduces both memory bandwidth consumption and kernel launch overhead.

## Full Name

**Kernel Fusion** (GPU Operator Fusion)

**Also Known As**: Operator fusion, graph-level optimization, kernel merging, op fusion

## Why Kernel Fusion Matters

### The Problem: Kernel Launch Overhead and Memory Traffic

On modern GPUs, a typical deep learning operation involves:

1. **Launch kernel A**: Read inputs from HBM → Compute → Write output to HBM
2. **Launch kernel B**: Read A's output from HBM → Compute → Write output to HBM
3. **Launch kernel C**: Read B's output from HBM → Compute → Write output to HBM

Each kernel launch incurs:
- **Launch overhead**: ~5-10 μs per kernel launch (significant for small operations)
- **Memory traffic**: Each intermediate result is written to and read from HBM (1.5-2 TB/s bandwidth, but still the bottleneck for memory-bound operations)
- **Synchronization**: GPU must finish one kernel before starting the next

### The Solution: Fused Kernel

A fused kernel combines A + B + C into a single launch:

1. **Launch fused kernel ABC**: Read inputs from HBM → Compute A in registers → Compute B in registers → Compute C in registers → Write final output to HBM

Intermediate results never leave fast on-chip memory, eliminating 2 round trips to HBM.

## Kernel Fusion in FlashAttention

[FlashAttention](term_flash_attention.md) fuses the entire attention computation into a single CUDA kernel:

### Unfused (Standard PyTorch) Attention: 5+ Kernel Launches

| Step | Kernel | HBM Read | HBM Write |
|------|--------|----------|-----------|
| 1 | $S = QK^T$ (matmul) | Q, K | S ($N^2$ elements) |
| 2 | $S = S / \sqrt{d}$ (scale) | S | S |
| 3 | $S = S + \text{mask}$ (mask) | S, mask | S |
| 4 | $P = \text{softmax}(S)$ (softmax) | S | P ($N^2$ elements) |
| 5 | $P = \text{dropout}(P)$ (dropout) | P | P |
| 6 | $O = PV$ (matmul) | P, V | O |
| **Total** | 6 kernels | Read S,P 3x each | Write S,P 3x each |

Total HBM traffic for intermediates: $\sim 6N^2$ elements (multiple reads/writes of $N \times N$ matrices).

### Fused (FlashAttention) Attention: 1 Kernel Launch

| Step | Location | Data |
|------|----------|------|
| Load $Q_i, K_j, V_j$ | HBM → SRAM | Block-sized tiles |
| Compute $S_{ij} = Q_i K_j^T / \sqrt{d}$ | SRAM (registers) | Never leaves on-chip |
| Apply mask | SRAM | Never leaves on-chip |
| Online softmax update ($m, \ell$) | SRAM | Never leaves on-chip |
| Apply dropout | SRAM | Never leaves on-chip |
| Accumulate $O_i$ | SRAM | Never leaves on-chip |
| Write $O_i, \ell_i, m_i$ | SRAM → HBM | Final output only |
| **Total** | 1 kernel | Read Q,K,V once; Write O once |

Total HBM traffic: $\Theta(Nd)$ for reading Q,K,V and writing O — the $N^2$-sized intermediates are eliminated entirely.

## Types of Kernel Fusion

### 1. Element-wise Fusion

Combine element-wise operations (add, multiply, activation functions):
```
# Unfused: 3 kernels
y = x + bias        # kernel 1
y = relu(y)          # kernel 2
y = y * scale        # kernel 3

# Fused: 1 kernel
y = relu(x + bias) * scale  # 1 kernel, intermediates in registers
```

### 2. Reduction Fusion

Combine reductions (softmax, layer norm, batch norm) with surrounding operations:
```
# Unfused: softmax alone is 3 passes (max, exp-sum, normalize)
# Fused: softmax + matmul in single kernel (FlashAttention)
```

### 3. Memory-Bound Fusion

Combine compute-light operations with memory-heavy operations to improve arithmetic intensity. This is the most impactful type — [FlashAttention](term_flash_attention.md) is the canonical example.

## Frameworks and Tools

| Framework | Fusion Approach |
|-----------|----------------|
| **PyTorch 2.0 (torch.compile)** | TorchInductor generates fused Triton kernels automatically |
| **Triton** | Python DSL for writing fused GPU kernels without raw CUDA |
| **NVIDIA TensorRT** | Graph-level fusion for inference workloads |
| **XLA (JAX/TensorFlow)** | HLO-level operation fusion |
| **FlashAttention** | Hand-written fused CUDA kernel for attention |
| **cuDNN** | Library-level fused operations (conv+bias+relu) |

## Performance Impact

Typical speedups from fusion (memory-bound operations):

| Operation | Unfused | Fused | Speedup |
|-----------|---------|-------|---------|
| LayerNorm + Residual + Dropout | 3 kernels | 1 kernel | 1.5-2x |
| Attention (scale + mask + softmax + dropout) | 5 kernels | 1 kernel | 2-4x |
| GELU + Bias + Residual | 3 kernels | 1 kernel | 1.3-1.8x |

The speedup is proportional to the ratio of eliminated HBM traffic to remaining HBM traffic.

## Limitations

- **Complexity**: Writing fused CUDA kernels requires deep GPU architecture knowledge
- **Portability**: Hand-fused kernels are often hardware-specific (A100 vs H100 vs AMD)
- **Register pressure**: Fusing too many operations can exhaust register files, causing **register spilling** to slow local memory
- **Occupancy**: Large fused kernels may reduce SM occupancy (fewer thread blocks fit)
- **Debugging**: Fused kernels are harder to debug and profile than individual operations

## Applications to Our Work

- **Model inference**: PyTorch 2.0's `torch.compile` automatically fuses operations in our deployed abuse detection models, providing 1.3-2x inference speedup
- **FlashAttention**: Our Transformer models benefit from FlashAttention's fused kernel for the attention bottleneck
- **Custom operations**: Understanding fusion helps when optimizing custom scoring or aggregation operations for real-time abuse detection

## Related Terms

- [FlashAttention](term_flash_attention.md) — Canonical example of attention kernel fusion
- [IO-Awareness](term_io_awareness.md) — Design principle that motivates kernel fusion
- [Tiling](term_tiling.md) — Complementary technique often combined with fusion
- [Online Softmax](term_online_softmax.md) — Enables softmax to be fused into the attention kernel
- [Transformer](term_transformer.md) — Architecture whose operations benefit most from fusion

## References

- Dao, T. et al. (2022). [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../papers/lit_dao2022flashattention.md). NeurIPS.
- Tillet, P. et al. (2019). Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations. MLSys.
- Ansel, J. et al. (2024). PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation. ASPLOS.
