---
tags:
  - resource
  - terminology
  - quantization
  - efficient_inference
  - model_compression
keywords:
  - GPTQ
  - Generative Pre-trained Transformer Quantization
  - weight quantization
  - Optimal Brain Surgeon
  - OBS
  - Hessian
  - layer-wise quantization
  - Int4
  - Int3
  - AutoGPTQ
topics:
  - Efficient Inference
  - Model Quantization
language: markdown
date of note: 2026-03-16
status: active
building_block: concept
---

# GPTQ (Generative Pre-trained Transformer Quantization)

## Definition

**GPTQ** is a one-shot, post-training weight quantization method that uses approximate second-order (Hessian) information to make optimal rounding decisions when compressing neural network weights to low-bit representations (typically Int4 or Int3). Developed by Elias Frantar, Saleh Ashkboos, Torsten Hoefler, and Dan Alistarh (2022), GPTQ was published at ICLR 2023. The method builds on the **Optimal Brain Surgeon (OBS)** framework and its quantization extension, Optimal Brain Quantization (OBQ), scaling them to models with hundreds of billions of parameters.

GPTQ achieves its efficiency by formulating weight quantization as a layer-wise reconstruction problem: for each layer, find quantized weights that minimize the squared error between the original and quantized layer outputs. By leveraging the inverse Hessian matrix of the layer-wise reconstruction loss, GPTQ compensates unquantized weights for the rounding error introduced by each newly quantized weight, distributing the error optimally across remaining weights.

The method is notable for being the first approach to quantize models at the 175B-parameter scale (OPT-175B, BLOOM-176B) to 4-bit and 3-bit precision with negligible accuracy degradation, completing the process in approximately 4 GPU-hours on a single NVIDIA A100. This enabled running a 175B-parameter model on a single GPU for generative inference for the first time.

## Algorithm

GPTQ processes the weight matrix of each linear layer independently, quantizing all rows simultaneously:

- **Layer-wise quantization**: Each Transformer layer is loaded into GPU memory and quantized independently. The objective is to minimize the squared error between the original layer output and the quantized layer output over a small calibration set (typically 128 samples from C4 or WikiText2).
- **Optimal Brain Quantization (OBQ) foundation**: For each weight being quantized, the algorithm computes the optimal rounding direction and distributes a compensation term to all remaining unquantized weights in the same row. The compensation is derived from the inverse Hessian of the reconstruction loss: delta_F = -(quant(w_q) - w_q) / [H^{-1}]_{qq} * H^{-1}_{q,:}, where H is the Hessian matrix.
- **Arbitrary order processing**: Unlike the original OBQ, which selects weights to quantize in a greedy order (most quantization-friendly first), GPTQ processes columns in sequential (left-to-right) order. This simplification has negligible impact on accuracy but enables massive computational savings through batched operations.
- **Lazy batch updates**: Columns are grouped into blocks of size B (typically B=128). Weight updates from quantizing columns within a block are accumulated lazily and applied to the remaining columns in a single batched update at the end of each block, dramatically improving GPU utilization.
- **Cholesky-based Hessian**: The inverse Hessian H^{-1} is computed efficiently using Cholesky decomposition, with rows and columns removed as weights are quantized. A small dampening term (1% of the average diagonal) is added for numerical stability.

## Key Properties

- **Weight-only quantization**: Quantizes model weights only; activations remain in FP16 during inference, with weights dequantized on-the-fly
- **Int4 and Int3 precision**: Primary target is 4-bit (3.25x compression vs FP16) and 3-bit (4.33x compression), with experimental 2-bit results
- **Scales to 175B parameters**: Quantizes OPT-175B in approximately 4 GPU-hours on a single A100, compared to days for prior second-order methods
- **Per-group quantization**: Supports grouping (e.g., g=128) where each group of consecutive weights shares its own scale and zero-point, improving accuracy at moderate overhead
- **Negligible perplexity loss at Int4**: OPT-175B loses only ~0.03 perplexity at 4-bit on WikiText2 compared to the FP16 baseline
- **No retraining required**: Purely post-training; needs only a small calibration set (128 samples) to compute the Hessian
- **Open-source ecosystem**: Widely adopted through AutoGPTQ and GPTQModel libraries, integrated into Hugging Face Transformers
- **Foundation for GGML/llama.cpp**: GPTQ-quantized models are commonly converted to GGUF format for CPU inference in the llama.cpp ecosystem

## Performance

| Model | Precision | WikiText2 PPL | PPL Degradation | Quantization Time |
|-------|-----------|---------------|-----------------|-------------------|
| OPT-175B | FP16 (baseline) | 8.34 | -- | -- |
| OPT-175B | Int4 (g=128) | 8.37 | +0.03 | ~4 hours |
| OPT-175B | Int3 (g=128) | 8.68 | +0.34 | ~4 hours |
| BLOOM-176B | FP16 (baseline) | 8.11 | -- | -- |
| BLOOM-176B | Int4 (g=128) | 8.29 | +0.18 | ~4 hours |
| BLOOM-176B | Int3 (g=128) | 8.65 | +0.54 | ~4 hours |

Inference speedups of approximately 3.25x on NVIDIA A100 and 4.5x on NVIDIA A6000 compared to FP16, driven by reduced memory bandwidth requirements for weight loading. GPTQ more than doubles the compression gains relative to previously proposed one-shot quantization methods while maintaining accuracy. At the extreme end, GPTQ also provides reasonable accuracy for 2-bit (ternary) quantization, though with more noticeable degradation.

## Comparison with Other Methods

| Method | Bit Width | Quantization Target | Key Technique | Speed to Quantize | Accuracy at Int4 |
|--------|-----------|---------------------|---------------|-------------------|-------------------|
| **RTN** (Round-to-Nearest) | Int4/Int8 | Weights | Naive rounding | Seconds | Poor (high PPL loss) |
| **GPTQ** | Int4/Int3 | Weights | Hessian-based optimal rounding | Hours (~4h for 175B) | Excellent (<0.5 PPL loss) |
| **LLM.int8()** | Int8 | Weights + Activations | Mixed-precision decomposition for outliers | Minutes | N/A (Int8 only) |
| **AWQ** | Int4 | Weights | Activation-aware per-channel scaling | Hours | Excellent (comparable to GPTQ) |

RTN serves as the simplest baseline with no error compensation. GPTQ significantly outperforms RTN at Int4, especially for smaller models. AWQ achieves comparable accuracy to GPTQ using a different philosophy (protecting salient channels rather than Hessian-based compensation). LLM.int8() operates at higher precision (Int8) and uniquely handles activation outliers via mixed-precision decomposition.

## Challenges and Limitations

- **Weight-only quantization**: Does not quantize activations, so it cannot leverage INT4 tensor-core arithmetic for the matrix multiply itself; speedup comes solely from reduced memory bandwidth
- **Calibration data sensitivity**: Quality and representativeness of the calibration set can affect quantization quality; mismatched calibration data may degrade results on target tasks
- **Slower quantization than RTN**: The Hessian computation and iterative weight updates require hours versus seconds for simple round-to-nearest, making rapid experimentation slower
- **Group size tradeoff**: Smaller group sizes (g=64, g=32) improve accuracy but increase storage overhead for per-group scale/zero-point constants, partially negating compression gains
- **Does not handle activation outliers**: Unlike LLM.int8() or SmoothQuant, GPTQ has no mechanism to address emergent outlier features in activations, which can limit combined W+A quantization

## Related Terms

- [Quantization](term_quantization.md) — Parent concept covering weight and activation quantization techniques
- [PTQ](term_ptq.md) — The broader post-training quantization category that GPTQ belongs to
- [QLoRA](term_qlora.md) — Alternative approach combining 4-bit NF4 quantization of the base model with 16-bit LoRA adapter fine-tuning
- [LoRA](term_lora.md) — Parameter-efficient fine-tuning method; can be applied on top of GPTQ-quantized models
- [Knowledge Distillation](term_knowledge_distillation.md) — Alternative model compression technique using teacher-student training
- [Transformer](term_transformer.md) — Target architecture whose linear layers GPTQ quantizes
- [LLM.int8()](term_llm_int8.md) — Complementary Int8 method with mixed-precision decomposition for activation outliers
- [AWQ](term_awq.md) — Alternative Int4 weight quantization method using activation-awareness rather than Hessian information

## References

### Vault Sources

- [LLM.int8() Literature Note](../papers/lit_dettmers2022llm.md) — Dettmers et al. (2022); discusses GPTQ as related work in the weight quantization landscape

### External Sources

- Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2022). GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers. ICLR 2023. [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)
- [AutoGPTQ GitHub Repository](https://github.com/AutoGPTQ/AutoGPTQ) — Popular open-source implementation of the GPTQ algorithm with broad model support
- [IST-DASLab Official GPTQ Repository](https://github.com/IST-DASLab/gptq) — Original research code from the paper authors
- [Hugging Face GPTQ Integration](https://huggingface.co/docs/transformers/en/quantization/gptq) — Documentation for using GPTQ-quantized models in the Transformers library
