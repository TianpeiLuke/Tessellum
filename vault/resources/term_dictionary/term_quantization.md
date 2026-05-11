---
tags:
  - resource
  - terminology
  - deep_learning
  - efficient_inference
  - model_compression
keywords:
  - quantization
  - post-training quantization
  - PTQ
  - quantization-aware training
  - QAT
  - absmax quantization
  - zero-point quantization
  - mixed-precision
  - Int8
  - Int4
  - NF4
  - weight quantization
  - activation quantization
  - bitsandbytes
  - GPTQ
  - AWQ
topics:
  - Deep Learning
  - Efficient Inference
  - Model Compression
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Term: Quantization

## Definition

**Quantization** is a model compression technique that maps high-precision numerical representations (typically 32-bit or 16-bit floating point) to lower-precision formats (8-bit integers, 4-bit integers, or custom data types) in order to reduce memory footprint, accelerate inference, and lower hardware cost. In the context of neural networks, quantization can be applied to **weights** (the learned parameters stored in each layer), **activations** (the intermediate tensor values computed during the forward pass), or both. The fundamental tradeoff is between numerical precision and computational efficiency: a well-designed quantization scheme preserves nearly all of the model's accuracy while achieving 2-8x compression and significant speedup through integer arithmetic, reduced memory bandwidth, and smaller cache footprints. Quantization has become indispensable for deploying large language models (LLMs) on commodity hardware, enabling models with tens or hundreds of billions of parameters to run on single consumer GPUs or even CPUs.

## Full Name

**Quantization** (Model Quantization, Neural Network Quantization)

**Also Known As**: Weight quantization, model compression, precision reduction, low-bit inference

## Quantization Fundamentals

### Absmax (Symmetric) Quantization

Absmax quantization maps a floating-point tensor $X$ to signed integers by dividing by the absolute maximum value and scaling to the target integer range. For Int8:

$$x_{\text{int8}} = \text{round}\!\left(\frac{127 \cdot x}{\max(|X|)}\right)$$

**Dequantization** recovers an approximation of the original value:

$$\hat{x} = \frac{\max(|X|)}{127} \cdot x_{\text{int8}}$$

The **scaling constant** $s = \max(|X|) / 127$ is stored alongside the quantized tensor. This scheme is **symmetric** because the zero point of the floating-point range maps exactly to integer zero, and the representable range is symmetric around zero: $[-127s, +127s]$.

### Zero-Point (Asymmetric) Quantization

Zero-point quantization handles asymmetric distributions by introducing an offset (zero-point) $z$:

$$x_{\text{int8}} = \text{round}\!\left(\frac{x - x_{\min}}{s}\right) + z$$

where:
- $s = \frac{x_{\max} - x_{\min}}{255}$ (scale factor for unsigned 8-bit)
- $z = \text{round}\!\left(-\frac{x_{\min}}{s}\right)$ (zero-point offset)

This maps the range $[x_{\min}, x_{\max}]$ to $[0, 255]$ (unsigned) or $[-128, 127]$ (signed), allowing the full integer range to be utilized even when the floating-point distribution is not centered at zero. Asymmetric quantization is more expressive but requires an additional zero-point constant per quantization group.

### Symmetric vs. Asymmetric Comparison

| Property | Symmetric (Absmax) | Asymmetric (Zero-Point) |
|----------|-------------------|------------------------|
| Parameters per group | 1 (scale only) | 2 (scale + zero-point) |
| Zero preservation | Exact (FP 0.0 maps to int 0) | Approximate |
| Range utilization | May waste range if distribution is skewed | Full range utilized |
| Compute overhead | Lower (no zero-point correction) | Higher (offset in matmul) |
| Typical use | Weights (roughly symmetric) | Activations (often asymmetric) |

### Quantization Granularity

The granularity at which scaling constants are computed controls the accuracy-overhead tradeoff:

- **Per-tensor**: One scale for the entire tensor. Fastest but least accurate.
- **Per-channel / Per-row**: One scale per output channel (Conv layers) or per row (linear layers). Standard for weight quantization.
- **Per-group / Per-block**: One scale per group of $g$ elements (e.g., $g = 64$ or $g = 128$). Used by GPTQ, AWQ, and QLoRA to improve accuracy at moderate overhead.
- **Per-element**: Theoretical maximum accuracy, but eliminates compression benefits.

## Taxonomy

### By Timing

| Approach | When Applied | Training Required | Calibration Data | Accuracy | Speed |
|----------|-------------|-------------------|-----------------|----------|-------|
| **Post-Training Quantization (PTQ)** | After training completes | No | Small set (100-1000 samples) | Good to excellent | Minutes to hours |
| **Quantization-Aware Training (QAT)** | During training/fine-tuning | Yes (full or partial) | Full training set | Best | Hours to days |
| **Dynamic Quantization** | At inference time per batch | No | None | Good | Fastest setup |

- **PTQ** is the most practical for large models — it requires no retraining, only a small calibration dataset to determine scaling constants. Methods like GPTQ and AWQ fall in this category.
- **QAT** inserts simulated quantization operations (fake quantization nodes) into the training graph so the model learns to be robust to quantization noise. This produces the highest accuracy but requires access to training infrastructure.
- **Dynamic quantization** computes scaling constants on-the-fly from each input batch. It adds slight runtime overhead but requires zero calibration data.

### By Target

| Target | What Is Quantized | Memory Savings | Speedup Source |
|--------|------------------|---------------|----------------|
| **Weight-only** | Model parameters | Proportional to bit reduction (e.g., 4x for FP16 to Int4) | Reduced memory bandwidth for weight loading |
| **Weight + Activation** | Parameters and intermediate values | Maximum | Integer arithmetic (INT8 matmul on tensor cores) |

Weight-only quantization is simpler and preserves more accuracy because weights have stable, well-characterized distributions. Activation quantization is harder due to outlier features and dynamic ranges that vary per input, but when achieved (e.g., SmoothQuant), it enables true integer-arithmetic speedups on hardware with INT8 tensor cores.

### By Granularity

| Granularity | Scale Constants | Overhead | Accuracy | Typical Use |
|-------------|----------------|----------|----------|-------------|
| **Per-tensor** | 1 per tensor | Minimal | Lowest | Dynamic quantization |
| **Per-channel / Per-row** | 1 per row or column | Low | Good | Standard weight PTQ |
| **Per-group (block)** | 1 per $g$ elements | Moderate | High | GPTQ ($g$=128), AWQ, QLoRA ($g$=64) |

## Key Methods

| Method | Year | Bit Width | Type | Key Innovation |
|--------|------|-----------|------|----------------|
| **LLM.int8()** | 2022 | Int8 | PTQ | Mixed-precision decomposition: identifies outlier features (>6.0 magnitude) in ~0.1% of hidden dimensions and keeps them in FP16, while quantizing remaining 99.9% to Int8. Eliminates emergent outlier degradation in models >6.7B parameters. |
| **GPTQ** | 2022 | Int4 / Int3 | PTQ | Optimal Brain Quantization applied layer-wise: uses approximate second-order (Hessian) information to find rounding decisions that minimize layer-wise reconstruction error. Quantizes 175B models in ~4 GPU-hours with negligible perplexity loss at 4-bit. |
| **AWQ** | 2023 | Int4 | PTQ | Activation-aware weight quantization: observes that ~1% of weight channels are disproportionately important (determined by activation magnitudes) and protects them via per-channel scaling before quantization. No backpropagation or reconstruction needed. |
| **QLoRA** | 2023 | NF4 | PTQ + LoRA | Introduces NormalFloat4 (NF4) data type optimal for normally-distributed weights, double quantization of scaling constants, and paged optimizers. Enables fine-tuning 65B models on a single 48GB GPU. |
| **SmoothQuant** | 2023 | Int8 W+A | PTQ | Migrates quantization difficulty from activations to weights via mathematically equivalent per-channel scaling transformation $Y = (X \text{diag}(s)^{-1}) \cdot (\text{diag}(s) W)$, making both weights and activations easy to quantize. Enables W8A8 with INT8 GEMM speedup. |
| **GGML / llama.cpp** | 2023 | Q2-Q8 | PTQ | Practical CPU-optimized quantization formats (Q4_0, Q4_1, Q5_0, Q5_1, Q8_0, etc.) with block-wise quantization ($g$=32). Enables LLM inference on consumer CPUs and Apple Silicon with AVX/NEON SIMD. |

## Data Types for Quantization

| Type | Bits | Exponent / Mantissa | Range (approx.) | Use Case |
|------|------|---------------------|-----------------|----------|
| **FP32** | 32 | 8e + 23m | $\pm 3.4 \times 10^{38}$ | Training (master weights), baseline reference |
| **FP16** | 16 | 5e + 10m | $\pm 65504$ | Mixed-precision training, inference |
| **BF16** | 16 | 8e + 7m | $\pm 3.4 \times 10^{38}$ | Training (same range as FP32, less precision); preferred on A100/H100 |
| **FP8 (E4M3)** | 8 | 4e + 3m | $\pm 448$ | Inference and training on H100; FlashAttention-3 support |
| **FP8 (E5M2)** | 8 | 5e + 2m | $\pm 57344$ | Gradient representation in FP8 training |
| **Int8** | 8 | N/A (integer) | $[-128, 127]$ | LLM.int8(), SmoothQuant, standard PTQ |
| **Int4** | 4 | N/A (integer) | $[-8, 7]$ | GPTQ, AWQ, weight-only quantization |
| **NF4** | 4 | N/A (lookup table) | 16 levels optimal for $\mathcal{N}(0,1)$ | QLoRA; information-theoretically optimal for normal weights |

### Memory Footprint Comparison (7B parameter model)

| Precision | Memory | Relative |
|-----------|--------|----------|
| FP32 | ~28 GB | 1.0x |
| FP16 / BF16 | ~14 GB | 0.5x |
| Int8 | ~7 GB | 0.25x |
| Int4 / NF4 | ~3.5 GB | 0.125x |

## Challenges and Limitations

### Outlier Features

Models above ~6.7B parameters develop **emergent outlier features** — a small number of hidden dimensions with magnitudes 10-100x larger than typical values. These outliers appear in specific feature dimensions across all sequence positions and layers. Standard quantization assigns disproportionate range to accommodate outliers, crushing the precision available for normal-magnitude values. Solutions include:
- **Mixed-precision decomposition** (LLM.int8()): Keep outlier dimensions in FP16
- **Activation smoothing** (SmoothQuant): Redistribute outlier magnitude from activations to weights
- **Clipping with learned ranges** (QAT): Learn optimal clipping thresholds

### Accuracy-Efficiency Tradeoff

- **4-bit weight-only**: Typically <1% perplexity degradation on well-calibrated methods (GPTQ, AWQ) for models >7B parameters
- **3-bit and below**: Significant degradation begins; active research area
- **Small models**: Quantization hurts small models (< 1B) more severely — fewer parameters mean less redundancy to absorb quantization noise
- **Task sensitivity**: Reasoning, math, and code generation tasks are more sensitive to quantization than general text generation

### Calibration Data Requirements

PTQ methods require representative calibration data to determine scaling constants and, in methods like GPTQ, to compute reconstruction targets. The calibration set should reflect the deployment distribution; mismatched calibration data can degrade accuracy. Typical requirements are modest (128-1024 samples for GPTQ/AWQ), but the choice of calibration data can materially impact results.

### Hardware and Software Ecosystem Fragmentation

Different hardware platforms support different quantized formats. INT8 tensor cores are available on NVIDIA GPUs from Turing onward, FP8 only on Hopper (H100), and INT4 GEMM support varies. CPU quantization (GGML, ONNX Runtime) and GPU quantization (bitsandbytes, TensorRT-LLM) use different formats, complicating deployment across heterogeneous infrastructure.

## Related Terms

- [PTQ](term_ptq.md) — Post-Training Quantization: the most practical quantization approach for LLMs, applied after training with no retraining required.
- [LLM.int8()](term_llm_int8.md) — Mixed-precision Int8 PTQ method with vector-wise quantization and outlier feature decomposition.
- [GPTQ](term_gptq.md) — Hessian-based weight quantization to Int4/Int3 using Optimal Brain Surgeon framework.
- [AWQ](term_awq.md) — Activation-aware weight quantization protecting salient channels via per-channel scaling.
- [Knowledge Distillation](term_knowledge_distillation.md) — Complementary compression technique: a smaller student model learns from a larger teacher. Can be combined with quantization for maximum compression.
- [QLoRA](term_qlora.md) — Combines NF4 quantization of frozen base model with 16-bit LoRA adapter training, enabling fine-tuning of 65B+ models on a single GPU.
- [LoRA](term_lora.md) — Parameter-efficient fine-tuning method; combined with quantization in QLoRA to achieve both memory-efficient storage and memory-efficient adaptation.
- [Scaling Law](term_scaling_law.md) — Quantization enables practical deployment of models at the scale predicted by scaling laws, bridging the gap between optimal training compute and inference budget.
- [Flash Attention](term_flash_attention.md) — Complementary memory optimization that reduces attention memory from $O(N^2)$ to $O(N)$; orthogonal to quantization and often used together.
- [Transformer](term_transformer.md) — Primary target architecture for quantization; the linear layers in attention and MLP blocks are the main quantization targets.
- [Data Parallelism](term_data_parallelism.md) — Quantization reduces per-device memory, potentially allowing larger batch sizes per GPU or reducing the number of GPUs needed for data-parallel training/inference.
- [Model Parallelism](term_model_parallelism.md) — Alternative strategy for fitting large models across multiple devices; quantization can reduce or eliminate the need for model parallelism by shrinking the model to fit on fewer devices.
- **[PyTorch](term_pytorch.md)**: PyTorch provides built-in quantization APIs (dynamic, static, QAT) for model compression and efficient inference

## Vault Sources

- [LLM.int8() — Model](../papers/paper_dettmers2022llm_model.md) — Dettmers et al. (2022). Foundational work on Int8 quantization for Transformers with mixed-precision decomposition for outlier features.

## References

### Primary Sources
- Dettmers, T., Lewis, M., Belkada, Y., & Zettlemoyer, L. (2022). LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. NeurIPS 2022. arXiv:2208.07339. *First to identify emergent outlier features and solve them with mixed-precision decomposition.*
- Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2022). GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers. ICLR 2023. arXiv:2210.17323. *Hessian-based optimal rounding enabling practical 4-bit and 3-bit quantization of 175B models.*
- Lin, J., Tang, J., Tang, H., Yang, S., Dang, X., & Han, S. (2023). AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration. MLSys 2024. arXiv:2306.00978. *Activation-aware scaling for weight-only Int4 quantization without backpropagation.*

### Extensions and Related Work
- Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient Finetuning of Quantized Language Models. NeurIPS 2023. arXiv:2305.14314. *NF4 data type, double quantization, and paged optimizers for quantized fine-tuning.*
- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., & Han, S. (2023). SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models. ICML 2023. arXiv:2211.10438. *Per-channel smoothing to enable W8A8 integer inference.*
- Jacob, B., Kligys, S., Chen, B., Zhu, M., et al. (2018). Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. CVPR 2018. arXiv:1712.05877. *Early foundational work on quantization-aware training for deployment.*

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | Maps high-precision (FP32/FP16) neural network values to lower-precision (Int8/Int4/NF4) representations |
| **Why** | Reduces memory footprint 2-8x, enables faster inference, lowers deployment cost |
| **Weight quantization** | Compresses stored parameters; stable distributions make this relatively straightforward |
| **Activation quantization** | Compresses intermediate values; harder due to outliers and dynamic ranges |
| **PTQ** | Applied after training with small calibration set; most practical for LLMs (GPTQ, AWQ, LLM.int8()) |
| **QAT** | Simulates quantization during training; highest accuracy but requires training infrastructure |
| **Key challenge** | Emergent outlier features in large models break naive quantization; solved by mixed-precision, smoothing, or activation-aware methods |
| **Ecosystem** | bitsandbytes (GPU Int8/NF4), GPTQ/AutoGPTQ (GPU Int4), llama.cpp/GGML (CPU), TensorRT-LLM (NVIDIA optimized) |
| **Complementary techniques** | [Flash Attention](term_flash_attention.md) (memory), [Knowledge Distillation](term_knowledge_distillation.md) (compression), [LoRA](term_lora.md)/[QLoRA](term_qlora.md) (efficient adaptation) |
