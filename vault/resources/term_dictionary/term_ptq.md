---
tags:
  - resource
  - terminology
  - model_compression
  - efficient_inference
  - quantization
keywords:
  - post-training quantization
  - PTQ
  - calibration
  - weight quantization
  - activation quantization
  - absmax
  - zero-point
  - round-to-nearest
  - optimal brain quantization
topics:
  - Efficient Inference
  - Model Compression
language: markdown
date of note: 2026-03-16
status: active
building_block: concept
---

# Post-Training Quantization (PTQ)

## Definition

**Post-Training Quantization (PTQ)** is a family of model compression techniques that convert a fully trained neural network from high-precision floating-point representations (FP32 or FP16) to lower-precision formats (Int8, Int4, or custom types) *without any retraining or gradient computation*. Unlike Quantization-Aware Training (QAT), which embeds simulated quantization into the training loop so the model can learn to compensate for quantization noise, PTQ operates entirely on a frozen, pre-trained model. This makes PTQ the dominant quantization paradigm for large language models, where the cost of retraining is prohibitive.

PTQ typically requires only a small **calibration dataset** (100-1024 unlabeled samples) to estimate the statistical properties of weights and activations, from which quantization scaling constants and zero-points are derived. The entire quantization process completes in minutes to hours rather than the days or weeks needed for QAT, making it thousands of times faster in practice. For models above roughly 6-7B parameters, well-designed PTQ methods (GPTQ, AWQ, SmoothQuant) achieve accuracy within 1% of the full-precision baseline at 4-bit or 8-bit precision.

PTQ should also be distinguished from **dynamic quantization**, which computes scaling constants on-the-fly at inference time for each input batch. Dynamic quantization requires no calibration data at all but introduces runtime overhead and cannot quantize weights ahead of time for storage savings in the same way static PTQ can.

## Key Properties

- **No retraining required** — operates on a frozen, pre-trained model with no backpropagation, making it applicable even when training data or infrastructure is unavailable.
- **Calibration-based** — uses a small representative dataset (typically 128-1024 samples) to collect activation statistics and determine optimal scaling constants.
- **Fast application** — quantizes models in minutes to hours, compared to days or weeks for QAT; thousands of times faster in practice.
- **Accuracy tradeoff** — generally incurs slightly more degradation than QAT, especially at very low bit widths (3-bit or below) or on small models (<1B parameters) where redundancy is limited.
- **Weight-only vs. weight+activation** — weight-only PTQ (GPTQ, AWQ) is simpler and more accurate because weight distributions are stable; weight+activation PTQ (SmoothQuant, LLM.int8()) enables true integer-arithmetic speedup but must handle dynamic activation ranges and outlier features.
- **Granularity options** — scaling constants can be computed per-tensor, per-channel, or per-group (block sizes of 64-128 elements), trading overhead for accuracy.
- **Hardware compatibility** — quantized formats must match target hardware capabilities (INT8 tensor cores from Turing onward, FP8 on Hopper, INT4 support varies).
- **Composable** — PTQ is orthogonal to and combinable with other optimizations such as Flash Attention, KV-cache compression, and [speculative decoding](term_speculative_decoding.md).

## Taxonomy

| Method | Year | Bit Width | Approach | Key Innovation |
|--------|------|-----------|----------|----------------|
| **RTN (Round-to-Nearest)** | Baseline | Any | Naive rounding | Rounds each weight to the nearest quantized value independently; simplest but lowest accuracy. |
| **GPTQ** | 2022 | Int4 / Int3 | Hessian / second-order | Applies Optimal Brain Quantization layer-wise using approximate Hessian information to minimize reconstruction error; quantizes 175B models in ~4 GPU-hours. |
| **OBQ (Optimal Brain Quantization)** | 2022 | Int4 | Hessian / second-order | Row-wise weight quantization using second-order curvature; GPTQ is its scalable successor. |
| **LLM.int8()** | 2022 | Int8 mixed | Mixed-precision decomposition | Identifies emergent outlier features (>6.0 magnitude in ~0.1% of dimensions) and keeps them in FP16, quantizing the remaining 99.9% to Int8. |
| **SmoothQuant** | 2023 | W8A8 | Activation-aware smoothing | Migrates quantization difficulty from activations to weights via per-channel scaling transformation, enabling W8A8 integer GEMM speedup. |
| **AWQ** | 2023 | Int4 | Activation-aware weighting | Identifies ~1% of weight channels that are disproportionately important (by activation magnitude) and protects them via per-channel scaling before quantization. MLSys 2024 Best Paper. |
| **GGML / llama.cpp** | 2023 | Q2-Q8 | Block-wise CPU-optimized | Practical quantization formats (Q4_0, Q4_1, Q5_K, etc.) with block size 32, optimized for CPU inference with AVX/NEON SIMD. |

## Calibration

Calibration is the process by which PTQ methods determine the quantization parameters (scale factors and zero-points) from a representative dataset. During calibration, the pre-trained model processes a batch of unlabeled samples while **Observer modules** collect statistics about activation ranges, means, and variances at each layer. No gradient computation or weight update occurs.

The calibration dataset should be **representative of the deployment distribution**. Mismatched calibration data (e.g., calibrating on English text but deploying on code) can materially degrade accuracy. Typical sample sizes range from 128 to 1024 examples; beyond this, returns diminish rapidly. More sophisticated methods like GPTQ use calibration data to compute Hessian approximations for optimal rounding decisions, while simpler methods like RTN only need activation ranges.

Calibration sensitivity is a known limitation: the choice of calibration samples can shift perplexity by 0.1-0.5 points, and certain domains (math, code) are more sensitive than others. Recent work on statistical pre-calibration approaches aims to reduce this variance.

## PTQ vs QAT Comparison

| Dimension | PTQ | QAT |
|-----------|-----|-----|
| **Training required** | No (frozen model) | Yes (full or partial fine-tuning) |
| **Calibration data** | 128-1024 unlabeled samples | Full training dataset |
| **Time to quantize** | Minutes to hours | Hours to days |
| **Accuracy at Int8** | Near-lossless | Best (near-lossless) |
| **Accuracy at Int4** | Good (within ~1% for large models) | Superior (~0.5% or less degradation) |
| **Accuracy at Int2-3** | Significant degradation | Recoverable with fine-tuning |
| **Applicable model scale** | Best for large models (>6B) | Any scale, but costly for large models |
| **Typical methods** | GPTQ, AWQ, SmoothQuant, LLM.int8() | LSQ, PACT, fake-quantization fine-tuning |
| **Practical use case** | Deploying open-source LLMs | When highest accuracy is paramount |

A well-tuned PTQ model can serve as a strong initialization for subsequent QAT fine-tuning, combining the speed of PTQ with the accuracy recovery of QAT.

## Challenges and Limitations

- **Emergent outlier features** — Models above ~6.7B parameters develop a small number of hidden dimensions with magnitudes 10-100x larger than typical values, breaking naive quantization schemes and requiring mixed-precision or smoothing solutions.
- **Calibration data sensitivity** — The choice and distribution of calibration samples can meaningfully affect quantized model quality; domain mismatch between calibration and deployment data leads to degradation.
- **Small model degradation** — Models with fewer than ~1B parameters have less redundancy to absorb quantization noise, making PTQ at 4-bit substantially more damaging than for larger models.
- **Hardware ecosystem fragmentation** — INT8 tensor cores (Turing+), FP8 (Hopper), INT4 GEMM support, and CPU quantization formats (GGML, ONNX Runtime) each require different quantization configurations, complicating cross-platform deployment.
- **Task sensitivity** — Reasoning, mathematics, and code generation tasks are more sensitive to quantization than general text generation, and PTQ degradation is not uniform across benchmarks.
- **Limited activation quantization** — Weight-only PTQ is well-solved, but quantizing activations remains challenging due to dynamic ranges and per-input variation, limiting the speedup achievable without techniques like SmoothQuant.

## Related Terms

- [Quantization](term_quantization.md) — parent concept covering all quantization approaches including PTQ, QAT, and dynamic quantization
- [QLoRA](term_qlora.md) — combines NF4 quantization with LoRA fine-tuning for memory-efficient adaptation
- [LoRA](term_lora.md) — parameter-efficient fine-tuning method, complementary to PTQ for adapting quantized models
- [Knowledge Distillation](term_knowledge_distillation.md) — alternative compression technique via teacher-student training
- [Flash Attention](term_flash_attention.md) — complementary memory optimization, orthogonal to quantization
- [Transformer](term_transformer.md) — target architecture whose linear layers are the primary quantization targets
- [Scaling Law](term_scaling_law.md) — PTQ enables deploying compute-optimal models predicted by scaling laws on constrained hardware
- [LLM.int8()](term_llm_int8.md) — mixed-precision Int8 PTQ method with outlier decomposition
- [GPTQ](term_gptq.md) — Hessian-based Int4 PTQ method using Optimal Brain Quantization
- [AWQ](term_awq.md) — activation-aware Int4 PTQ method protecting salient weight channels

## References

### Vault Sources

- [LLM.int8() Paper](../papers/lit_dettmers2022llm.md) — Dettmers et al. (2022). Foundational work on Int8 matrix multiplication for Transformers with mixed-precision decomposition.

### External Sources

- Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2022). [GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers](https://arxiv.org/abs/2210.17323). ICLR 2023.
- Lin, J., Tang, J., Tang, H., Yang, S., Dang, X., & Han, S. (2023). [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://github.com/mit-han-lab/llm-awq). MLSys 2024 Best Paper.
- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., & Han, S. (2023). [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/abs/2211.10438). ICML 2023.
- Gholami, A., Kim, S., Dong, Z., et al. (2021). [A Survey of Quantization Methods for Efficient Neural Network Inference](https://arxiv.org/abs/2103.13630). Comprehensive survey covering PTQ and QAT fundamentals.
- [Practical Guide to LLM Quantization Methods](https://cast.ai/blog/demystifying-quantizations-llms/) — Cast AI. Practical overview comparing GPTQ, AWQ, SmoothQuant, and LLM.int8() for LLM deployment.
