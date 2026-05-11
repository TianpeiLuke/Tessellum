---
tags:
  - resource
  - terminology
  - quantization
  - efficient_inference
  - transformer_architecture
keywords:
  - LLM.int8()
  - 8-bit inference
  - vector-wise quantization
  - mixed-precision decomposition
  - emergent features
  - outlier features
  - bitsandbytes
  - Int8 matrix multiplication
topics:
  - Efficient Inference
  - Model Quantization
language: markdown
date of note: 2026-03-16
status: active
building_block: concept
---

# LLM.int8()

## Definition

**LLM.int8()** is a post-training quantization method developed by Tim Dettmers, Mike Lewis, Younes Belkada, and Luke Zettlemoyer (NeurIPS 2022) that enables 8-bit integer inference for transformer feed-forward and attention projection layers with zero performance degradation at scales up to 175B parameters. The method combines two complementary techniques: **vector-wise quantization** (per-row scaling for activations, per-column scaling for weights) and **mixed-precision decomposition** (isolating outlier feature dimensions into FP16 while quantizing the remaining 99.9% of values to Int8).

The key insight behind LLM.int8() is that naive Int8 quantization fails at scale not because of general numerical noise, but because of **emergent outlier features** --- a small number of hidden dimensions with magnitudes 20-100x the typical range that appear systematically once models exceed approximately 6.7B parameters. These outliers dominate the scaling constants in standard quantization, crushing the precision available for all other values. Rather than improving the quantization scheme uniformly, LLM.int8() separates outliers for exact FP16 treatment while aggressively quantizing everything else.

LLM.int8() is implemented in the open-source **bitsandbytes** library and has become foundational infrastructure for the LLM ecosystem, serving as the basis for QLoRA and the broader Hugging Face quantization integration. It halves the GPU memory required for inference, enabling models like OPT-175B and BLOOM-176B to run on a single server with consumer GPUs.

## Algorithm

### Part 1: Vector-wise Quantization

For a matrix multiplication $Y = X \cdot W^T$ where $X \in \mathbb{R}^{b \times h}$ (activations) and $W \in \mathbb{R}^{o \times h}$ (weights):

1. Compute per-row scaling constants for activations: $c_{X_i} = \max_j(|X_{ij}|) / 127$
2. Compute per-column scaling constants for weights: $c_{W_j} = \max_i(|W_{ij}|) / 127$
3. Quantize both to Int8: $X_{\text{int8}} = \lfloor X / c_X \rceil$, $W_{\text{int8}} = \lfloor W / c_W \rceil$
4. Multiply in Int8: $Y_{\text{int8}} = X_{\text{int8}} \cdot W_{\text{int8}}^T$
5. Denormalize via outer product: $\hat{Y}_{ij} = Y_{\text{int8}_{ij}} \cdot c_{X_i} \cdot c_{W_j}$

Vector-wise quantization provides approximately 2x better precision than tensor-wise quantization with negligible overhead, since the denormalization step (5) requires only an outer product $c_X \otimes c_W$ of two vectors.

### Part 2: Mixed-Precision Decomposition

For dimensions containing outlier values (magnitude exceeding threshold $\alpha = 6.0$ standard deviations):

1. **Detect outlier dimensions**: Identify column indices $O = \{j : |X_{ij}| > \alpha\}$
2. **Decompose**: Split X and W into outlier ($X_O$, $W_O$) and normal ($X_N$, $W_N$) subsets
3. **Compute separately and combine**:

$$Y = \underbrace{X_O \cdot W_O^T}_{\text{FP16}} + \underbrace{(X_{N,\text{int8}} \cdot W_{N,\text{int8}}^T) \cdot c_X \cdot c_W}_{\text{Int8 with dequantization}}$$

At the optimal threshold $\alpha = 6.0$, outlier dimensions comprise less than 1% of total dimensions but account for over 10% of total activation magnitude. Weight quantization is performed offline (once), while activation quantization occurs at runtime.

## Emergent Outlier Features

The paper's most significant scientific contribution is the discovery and characterization of emergent outlier features in transformer activations:

- **Phase transition at ~6.7B parameters**: Below this scale, outlier dimensions appear probabilistically with ~60% layer agreement. Above it, 100% of layers use identical outlier dimensions --- a sharp phase transition.
- **Extreme concentration**: In a 6.7B model, approximately **150,000 outlier values** per sequence are concentrated in just **6 hidden dimensions** out of 4,096, present at 75% of sequence positions.
- **Extreme magnitude**: Outlier values are 20-100x the typical activation range, with consistent signs (always positive or always negative per dimension).
- **Systematic location**: Outliers appear in attention projection and first FFN layers; they are consumed by softmax and the second FFN layer. They likely encode global positional or structural information for token routing.
- **Quantization failure mechanism**: When outliers coexist with normal values, the absmax scaling constant is dominated by the outlier, mapping all normal values to a tiny fraction of the Int8 range. This information squashing causes ~8x higher quantization error in affected vectors.

## Key Properties

- **Zero degradation at scale**: Perplexity within 0.1 of FP16 for models up to 175B parameters
- **~2x memory reduction**: Consistently halves GPU memory across all tested model sizes
- **~5-15% speed overhead**: Due to the FP16 decomposition path; increases with model size
- **Threshold $\alpha = 6.0$**: Empirically optimal, capturing all important outliers while keeping >99% of values in Int8
- **No retraining required**: Pure post-training quantization; no calibration dataset needed beyond detecting outlier dimensions
- **Open-source**: Fully implemented in the [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) library with Hugging Face integration
- **Foundation for QLoRA**: The bitsandbytes library and Int8 infrastructure directly enabled QLoRA's 4-bit NF4 quantization for fine-tuning

## Performance

### Perplexity (WikiText2, lower is better)

| Model | FP16 | Naive Int8 | LLM.int8() | Degradation |
|-------|------|-----------|-------------|-------------|
| OPT-125M | 27.7 | 27.8 | 27.7 | 0.0% |
| OPT-1.3B | 14.6 | 14.7 | 14.6 | 0.0% |
| OPT-6.7B | 10.9 | 11.8 | 10.9 | 0.0% |
| OPT-13B | 10.1 | 11.2 | 10.1 | 0.0% |
| OPT-66B | 9.3 | 22.4 | 9.3 | 0.0% |
| OPT-175B | 10.7 | --- | 10.8 | +0.9% |
| BLOOM-176B | 24.2 | --- | 24.4 | +0.8% |

Naive Int8 degrades catastrophically beyond 6.7B parameters (OPT-66B: 22.4 vs 9.3 FP16), while LLM.int8() maintains near-zero degradation across all scales.

### Memory Reduction

| Model | FP16 Memory | LLM.int8() Memory | Reduction | Speed vs FP16 |
|-------|-------------|-------------------|-----------|---------------|
| OPT-6.7B | 13.4 GB | 6.8 GB | 1.97x | ~0.95x |
| OPT-13B | 26.1 GB | 13.2 GB | 1.98x | ~0.93x |
| OPT-66B | 132 GB | 67 GB | 1.97x | ~0.90x |
| OPT-175B | ~350 GB | ~180 GB | 1.94x | ~0.85x |

## Related Terms

- [Quantization](term_quantization.md) --- parent concept covering all precision-reduction techniques for neural networks
- [PTQ](term_ptq.md) --- post-training quantization, the broader category LLM.int8() belongs to
- [QLoRA](term_qlora.md) --- builds directly on the bitsandbytes library, extending to 4-bit NF4 with LoRA adapters
- [LoRA](term_lora.md) --- parameter-efficient fine-tuning method, combined with LLM.int8() infrastructure in QLoRA
- [Scaling Law](term_scaling_law.md) --- emergent outlier features are a scaling phenomenon with a sharp phase transition at 6.7B
- [Flash Attention](term_flash_attention.md) --- complementary memory optimization via IO-aware tiling; orthogonal to quantization
- [Transformer](term_transformer.md) --- target architecture; LLM.int8() applies to attention projection and FFN layers
- [GPTQ](term_gptq.md) --- alternative PTQ method using Hessian-based optimal rounding for weight-only Int4 quantization
- [AWQ](term_awq.md) --- alternative PTQ method using activation-aware scaling for weight-only Int4 quantization

## References

### Vault Sources

- [LLM.int8() Literature Note](../papers/lit_dettmers2022llm.md) --- full literature note with metadata, abstract, and paper structure
- [LLM.int8() Model](../papers/paper_dettmers2022llm_model.md) --- detailed technical description of the algorithm and design choices
- [LLM.int8() Experiment Results](../papers/paper_dettmers2022llm_exp_result.md) --- comprehensive results including ablation studies and phase transition analysis

### External Sources

- Dettmers, T., Lewis, M., Belkada, Y., & Zettlemoyer, L. (2022). LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. NeurIPS 2022. [arXiv:2208.07339](https://arxiv.org/abs/2208.07339).
- Tim Dettmers. [LLM.int8() and Emergent Features](https://timdettmers.com/2022/08/17/llm-int8-and-emergent-features/). Blog post, August 2022.
- [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) --- open-source library implementing LLM.int8() and related quantization methods for PyTorch.
