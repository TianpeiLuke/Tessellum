---
tags:
  - resource
  - terminology
  - multimodal
  - transformer
  - vision_language
  - cross_attention
keywords:
  - Q-Former
  - Querying Transformer
  - BLIP-2
  - modality bridging
  - cross-attention
  - learnable queries
  - vision-language
  - frozen encoder
topics:
  - Multimodal Learning
  - Model Architecture
  - Vision-Language Models
language: markdown
date of note: 2026-03-30
status: active
building_block: concept
---

# Q-Former (Querying Transformer)

## Definition

**Q-Former (Querying Transformer)** is a lightweight Transformer encoder architecture introduced in BLIP-2 (Li et al., 2023) that bridges the modality gap between frozen pre-trained encoders (e.g., vision) and frozen large language models. It uses a set of **learnable query embeddings** that interact with the encoder's output via cross-attention, extracting the most task-relevant information and producing a fixed set of "soft tokens" that the frozen LLM can condition on.

The key insight is that rather than training a massive multimodal model end-to-end, a small trainable bridge module (~188M parameters) can align heterogeneous modalities with dramatically fewer parameters — BLIP-2's Q-Former outperforms Flamingo80B by 8.7% on VQAv2 with **54× fewer trainable parameters**.

## Architecture

| Component | Specification |
|-----------|--------------|
| **Layers** | 12 Transformer layers |
| **Initialization** | BERT-base weights |
| **Learnable queries** | 32 queries × 768-dim |
| **Cross-attention** | Queries attend to frozen encoder outputs |
| **Self-attention** | Queries attend to each other and text tokens; mask pattern varies by objective |
| **Trainable params** | ~188M (Q-Former + projection layer) |
| **Output** | 32 fixed-size embeddings → FC projection → LLM embedding space |

## Key Properties

- **Modality-agnostic bridge**: While designed for vision-language, the Q-Former mechanism generalizes to any encoder→LLM bridging (vision, tabular, audio, graph)
- **Fixed output size**: Regardless of input resolution or sequence length, Q-Former always produces exactly 32 output embeddings — providing computational predictability
- **Multi-objective training via attention masks**: ITC, ITM, and ITG objectives share the same weights with different self-attention mask patterns
- **Frozen component compatibility**: Works with arbitrary frozen encoders and LLMs (ViT-L/G, OPT, FlanT5)
- **Two-stage bootstrapping**: Stage 1 aligns representations with the encoder; Stage 2 connects to the LLM

## Applications

| Domain | System | Adaptation |
|--------|--------|------------|
| **Vision-Language** | BLIP-2 | Original: image encoder → Q-Former → frozen LLM |
| **Abuse Prevention** | [SOPA](../../areas/models/model_sopa_llm.md) | Tabular encoder (customer profiles) → Tabular-Language Q-Former → frozen Phi-3 |
| **Video Understanding** | Video-LLaMA | Temporal Q-Former for video frames |
| **3D Understanding** | 3D-LLM | Point cloud encoder → Q-Former → LLM |

## Related Terms

- **[BLIP-2](term_blip2.md)**: The model that introduced Q-Former as its core architectural innovation
- **[Attention Mechanism](term_attention_mechanism.md)**: Cross-attention between queries and encoder outputs is the core mechanism
- **[Transformer](term_transformer.md)**: Q-Former is a standard Transformer encoder with added cross-attention layers
- **[BERT](term_bert.md)**: Q-Former is initialized from BERT-base weights
- **[Contrastive Learning](term_contrastive_learning.md)**: Image-Text Contrastive (ITC) is one of the three Q-Former pre-training objectives
- **[Foundation Model](term_foundation_model.md)**: Q-Former bridges frozen foundation models without fine-tuning them
- **[Zero-Shot Learning](term_zero_shot_learning.md)**: Q-Former enables zero-shot multimodal capabilities
- **[Phi](term_phi.md)**: Phi-3-mini serves as the frozen LLM in SOPA's Q-Former pipeline

## References

### Vault Sources

- [BLIP-2 Literature Note](../papers/lit_li2023blip2.md) — Original paper introducing Q-Former
- [SOPA LLM](../../areas/models/model_sopa_llm.md) — Production adaptation of Q-Former for tabular-language bridging

### External Sources

- [Li et al. (2023). "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models." ICML](https://arxiv.org/abs/2301.12597) — Original Q-Former paper (7,498 citations)
- [Hugging Face: BLIP-2 Documentation](https://huggingface.co/docs/transformers/model_doc/blip-2) — Implementation details and usage guide
