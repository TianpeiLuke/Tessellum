---
tags:
  - resource
  - terminology
  - machine_learning
  - nlp
  - parameter_efficient_fine_tuning
  - quantization
keywords:
  - QLoRA
  - quantized LoRA
  - 4-bit quantization
  - NormalFloat4
  - NF4
  - double quantization
  - paged optimizers
  - memory-efficient fine-tuning
  - Guanaco
  - Dettmers
topics:
  - Machine Learning
  - Natural Language Processing
  - Model Adaptation
  - Parameter-Efficient Fine-Tuning
  - Quantization
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: QLoRA — Quantized Low-Rank Adaptation

## Definition

**QLoRA** (Quantized Low-Rank Adaptation) is an extension of [LoRA](term_lora.md) that combines 4-bit quantization of the frozen base model with low-rank adapter training in 16-bit precision, enabling fine-tuning of large language models on consumer-grade hardware. Introduced by Dettmers et al. (2023), QLoRA introduces three technical innovations: (1) **NormalFloat4 (NF4)** data type — an information-theoretically optimal 4-bit quantization format for normally distributed weights, (2) **Double Quantization** — quantizing the quantization constants themselves to save ~0.37 bits per parameter, and (3) **Paged Optimizers** — using NVIDIA unified memory to handle memory spikes during gradient checkpointing. These innovations enable fine-tuning a 65B-parameter model on a single 48GB GPU while preserving 16-bit fine-tuning performance. QLoRA's Guanaco model family matched 99.3% of ChatGPT performance on the Vicuna benchmark while training on a single GPU in 24 hours.

## Full Name

**QLoRA** — Quantized Low-Rank Adaptation

**Also Known As**: Quantized LoRA, 4-bit LoRA

## Technical Approach

### Base Model Quantization

The frozen pre-trained weights W₀ are quantized from 16-bit to 4-bit using NormalFloat4:

1. **Normalize weights** to zero mean, unit variance per block (typically 64 weights per block)
2. **Map to NF4 levels**: 16 quantization levels optimally placed for a normal distribution (not uniformly spaced like standard INT4)
3. **Store quantization constants** (scale and zero-point per block) in 8-bit format
4. **Double quantization**: Further quantize the 8-bit constants to reduce overhead from 0.5 bits/param to 0.127 bits/param

### Training Pipeline

```
Forward pass:  Dequantize W₀ (4-bit → 16-bit) → compute h = W₀x + BAx
Backward pass: Gradients computed in 16-bit for A and B only
               W₀ gradients NOT computed (frozen)
Optimizer:     A, B updated in 16-bit; W₀ unchanged
```

The key insight: dequantization from 4-bit to 16-bit is computationally cheap (lookup table), so the forward pass overhead is minimal. Only the small LoRA matrices (A, B) maintain 16-bit precision and receive gradient updates.

## Memory Comparison

| Method | 65B Model Memory | Training Memory | Hardware |
|--------|-----------------|-----------------|----------|
| Full FT (16-bit) | ~130 GB | ~780 GB | 10+ A100-80GB |
| LoRA (16-bit base) | ~130 GB | ~160 GB | 2-3 A100-80GB |
| **QLoRA (4-bit base)** | **~33 GB** | **~48 GB** | **1 A100-48GB** |
| QLoRA (4-bit, 33B) | ~17 GB | ~24 GB | 1 RTX 4090 (24GB) |

## Key Results

| Model | Benchmark | Performance | vs. ChatGPT |
|-------|-----------|-------------|-------------|
| Guanaco 65B | Vicuna | 99.3% | ~equivalent |
| Guanaco 33B | Vicuna | 97.8% | competitive |
| Guanaco 7B | Vicuna | 85.7% | usable |

### Performance Preservation

QLoRA matches 16-bit LoRA performance across tasks despite 4-bit quantization of the base model. The NF4 data type preserves model quality because:
- Neural network weights are approximately normally distributed after pre-training
- NF4 places quantization levels to minimize expected quantization error for this distribution
- The LoRA adapters operate in full 16-bit precision, compensating for any quantization loss

## Key Findings Beyond Method

The paper also contributed a large-scale study of fine-tuning approaches:

1. **All-linear-layers LoRA outperforms Wq+Wv**: Applying LoRA to every linear layer (attention + MLP) consistently outperforms the original LoRA paper's Wq+Wv recommendation
2. **Data quality > quantity**: A 9K high-quality dataset (OASST1) outperforms a 450K low-quality dataset (FLAN v2) for chatbot training
3. **Chatbot evaluation**: Introduced a comprehensive evaluation framework finding that existing benchmarks poorly correlate with human chatbot preferences

## Applications to Our Work

- **Production deployment**: BRP uses QLoRA to fine-tune Falcon-40B on buyer-seller messaging data for abuse detection, reducing GPU memory from 80GB+ (full FT) to ~24GB (single GPU)
- **Rapid prototyping**: QLoRA enables data scientists to experiment with 40B+ models on single SageMaker instances, dramatically reducing iteration cycles for abuse model development
- **Cost efficiency**: Fine-tuning on a single GPU vs. a multi-GPU cluster reduces training costs by 5-10× while maintaining performance parity

## Related Terms

- [LoRA](term_lora.md) — Base method that QLoRA extends with quantization; W = W₀ + BA formulation
- [PEFT](term_peft.md) — Broader family; QLoRA is the most memory-efficient member
- [LLM](term_llm.md) — Target models; QLoRA makes 65B+ model fine-tuning accessible on consumer hardware
- [Fine-Tuning](term_fine_tuning.md) — QLoRA matches full fine-tuning quality while using 16× less memory
- [Intrinsic Dimensionality](term_intrinsic_dimensionality.md) — Theoretical basis for why low-rank adaptation works despite aggressive quantization
- [Transformer](term_transformer.md) — Architecture whose linear layers are quantized and adapted

## References

### Primary Source
- Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient Finetuning of Quantized Language Models. NeurIPS 2023. arXiv:2305.14314. *Introduced QLoRA with NF4, double quantization, and paged optimizers.*

### Foundations
- [LoRA (Hu et al., 2021)](../papers/lit_hu2021lora.md) — Original LoRA method that QLoRA builds upon.
- Dettmers, T. et al. (2022). LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. NeurIPS 2022. *Prior quantization work by the same first author.*

### Related Literature
- [Task-Agnostic Low-Rank Adapters (Xiao et al., 2023)](../papers/lit_xiao2023task.md) — HyperLoRA: another LoRA extension using hypernetworks for zero-shot transfer.
