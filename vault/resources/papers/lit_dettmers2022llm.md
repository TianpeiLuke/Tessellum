---
tags:
  - resource
  - literature_note
  - quantization
  - efficient_inference
  - transformer_architecture
keywords:
  - LLM.int8()
  - quantization
  - 8-bit inference
  - vector-wise quantization
  - mixed-precision decomposition
  - emergent features
  - outlier features
  - Int8 matrix multiplication
  - model compression
  - bitsandbytes
topics:
  - Efficient Inference
  - Model Quantization
  - Transformer Architecture
domain: "Efficient Inference"
language: markdown
date of note: 2026-03-15
paper_title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"
authors:
  - Tim Dettmers
  - Mike Lewis
  - Younes Belkada
  - Luke Zettlemoyer
year: 2022
source: "arXiv:2208.07339"
venue: "NeurIPS 2022"
doi: "10.48550/arXiv.2208.07339"
arXiv: "2208.07339"
semantic_scholar_id: "4be7d1524edb0137599a5cc95f72844b85a52fe1"
zotero_key: "CNWF7GM4"
paper_id: dettmers2022llm
paper_notes:
  - paper_dettmers2022llm_intro.md
  - paper_dettmers2022llm_contrib.md
  - paper_dettmers2022llm_model.md
  - paper_dettmers2022llm_exp_design.md
  - paper_dettmers2022llm_exp_result.md
status: active
building_block: hypothesis
---

# LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale |
| **Authors** | Tim Dettmers, Mike Lewis, Younes Belkada, Luke Zettlemoyer |
| **Year** | 2022 |
| **Venue** | NeurIPS 2022 |
| **arXiv** | [2208.07339](https://arxiv.org/abs/2208.07339) |
| **Semantic Scholar** | [4be7d15...](https://www.semanticscholar.org/paper/4be7d1524edb0137599a5cc95f72844b85a52fe1) |
| **Zotero** | CNWF7GM4 |
| **Citations** | ~906 |
| **Code** | [TimDettmers/bitsandbytes](https://github.com/TimDettmers/bitsandbytes) |

## Abstract

Large language models have been widely adopted but require significant GPU memory for inference. We develop a procedure for Int8 matrix multiplication for feed-forward and attention projection layers in transformers, which cut the GPU memory needed for inference by half while retaining full precision performance. Our method uses vector-wise quantization with separate normalization constants for each inner product in the matrix multiplication, to quantize most of the features. For the emergent outliers, we also include a new mixed-precision decomposition scheme, which isolates the outlier feature dimensions into a 16-bit matrix multiplication while still more than 99.9% of values are multiplied in 8-bit. Using LLM.int8(), we show empirically it is possible to perform inference in LLMs with up to 175B parameters without any performance degradation. This makes such models much more accessible, for example, it is possible to use OPT-175B/BLOOM on a single server with consumer GPUs.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_dettmers2022llm_intro](paper_dettmers2022llm_intro.md) | GPU memory bottleneck for LLM inference; quantization failure at scale due to emergent outlier features; gap in understanding systematic outliers |
| **Contribution** | [paper_dettmers2022llm_contrib](paper_dettmers2022llm_contrib.md) | Two-part quantization (vector-wise + mixed-precision decomposition); emergent feature analysis; zero-degradation Int8 inference up to 175B |
| **Model** | [paper_dettmers2022llm_model](paper_dettmers2022llm_model.md) | Absmax quantization; vector-wise row/column normalization; mixed-precision decomposition with α=6.0 threshold; outlier dimension isolation |
| **Experiment Design** | [paper_dettmers2022llm_exp_design](paper_dettmers2022llm_exp_design.md) | OPT (125M–175B), BLOOM-176B, GPT-2; WikiText2, C4; perplexity and zero-shot evaluation; ablation on threshold α |
| **Experiment Results** | [paper_dettmers2022llm_exp_result](paper_dettmers2022llm_exp_result.md) | Zero degradation at 175B scale; phase transition at 6.7B; 6 outlier dimensions contain 150K outliers; 2x memory reduction; α=6.0 optimal |
| **Review** | [review_dettmers2022llm](review_dettmers2022llm.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 8 questions (5 review lenses applied) |

## Summary

- **Background**: Large language models require prohibitive GPU memory for inference (OPT-175B needs ~350GB in FP16). Standard Int8 quantization fails at scale because transformer activations develop highly systematic emergent outlier features — large-magnitude values concentrated in a few dimensions — that standard quantization squashes, destroying model quality. <!-- VERIFY -->
- **Contribution**: LLM.int8() is a two-part quantization procedure that combines vector-wise quantization (per-row/column normalization constants instead of per-tensor) with mixed-precision decomposition (outlier dimensions computed in FP16, remaining 99.9% in Int8). The paper also provides the first systematic study of emergent outlier features in transformers and their phase transition at ~6.7B parameters. <!-- VERIFY -->
- **Model**: The method separates each matrix multiplication into two paths: outlier dimensions (magnitude > α=6.0 standard deviations) are extracted and computed in FP16, while the remaining dimensions use absmax Int8 quantization with vector-wise scaling constants `c_X` (row) and `c_W` (column). The output combines both paths: `y = X_outlier · W_outlier^T + (X_int8 · W_int8^T) · c_X · c_W`. <!-- VERIFY -->
- **Results**: LLM.int8() achieves zero-degradation inference for OPT-175B and BLOOM-176B (perplexity within 0.1 of FP16). A phase transition occurs at 6.7B parameters where outlier features become fully coordinated across all layers, concentrating in just 6 dimensions. Memory reduction is ~2x; the method enables OPT-175B inference on a single server with consumer GPUs. <!-- VERIFY -->

## Relevance to Our Work

- **[Knowledge Distillation](../term_dictionary/term_knowledge_distillation.md)**: Complementary model compression approach — distillation reduces parameters, LLM.int8() reduces precision; both enable deployment of large models
- **[QLoRA](../term_dictionary/term_qlora.md)**: QLoRA builds directly on LLM.int8() and the bitsandbytes library, combining 4-bit quantization with LoRA adapters for fine-tuning
- **[LoRA](../term_dictionary/term_lora.md)**: Both address LLM efficiency — LoRA reduces trainable parameters, LLM.int8() reduces inference memory
- **[Scaling Law](../term_dictionary/term_scaling_law.md)**: Emergent outlier features are a scaling phenomenon — they appear only beyond ~6.7B parameters, connecting to phase transitions in neural scaling
- **[Transformer](../term_dictionary/term_transformer.md)**: LLM.int8() targets the core Transformer operations (attention projections and FFN layers)

## Related Documentation

### Paper Notes
- [Introduction](paper_dettmers2022llm_intro.md)
- [Contribution](paper_dettmers2022llm_contrib.md)
- [Model](paper_dettmers2022llm_model.md)
- [Experiment Design](paper_dettmers2022llm_exp_design.md)
- [Experiment Results](paper_dettmers2022llm_exp_result.md)

### Related Vault Notes
- [Knowledge Distillation](../term_dictionary/term_knowledge_distillation.md) — complementary compression via teacher-student training
- [QLoRA](../term_dictionary/term_qlora.md) — builds on bitsandbytes for quantized fine-tuning
- [LoRA](../term_dictionary/term_lora.md) — parameter-efficient fine-tuning complementing quantized inference
- [Scaling Law](../term_dictionary/term_scaling_law.md) — emergent features as a scaling phenomenon
- [Transformer](../term_dictionary/term_transformer.md) — target architecture for quantization

### Related Literature
- Hu et al. (2021). "LoRA: Low-Rank Adaptation of Large Language Models" — [lit_hu2021lora](lit_hu2021lora.md) — parameter-efficient alternative to full fine-tuning
- Hoffmann et al. (2022). "Training Compute-Optimal Large Language Models" — [lit_hoffmann2022training](lit_hoffmann2022training.md) — Chinchilla scaling laws; LLM.int8() enables deploying compute-optimal models efficiently
