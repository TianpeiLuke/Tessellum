---
tags:
  - resource
  - terminology
  - multimodal
  - vision_language
  - efficient_pretraining
keywords:
  - BLIP-2
  - Bootstrapping Language-Image Pre-training
  - Q-Former
  - vision-language model
  - frozen models
  - Salesforce
  - multimodal
topics:
  - Multimodal Learning
  - Vision-Language Models
  - Efficient Pre-training
language: markdown
date of note: 2026-03-30
status: active
building_block: concept
---

# BLIP-2 (Bootstrapping Language-Image Pre-training 2)

## Definition

**BLIP-2** is a vision-language pre-training framework developed by Salesforce Research (Li et al., 2023) that achieves state-of-the-art multimodal performance by training only a lightweight **Querying Transformer (Q-Former)** between frozen pre-trained image encoders and frozen large language models. Published at ICML 2023, BLIP-2 outperforms Flamingo80B by 8.7% on zero-shot VQAv2 with 54× fewer trainable parameters (~188M vs 10.2B).

The key innovation is the insight that multimodal AI does not require end-to-end training of massive models — a small trainable bridge module can align existing unimodal representations more effectively and efficiently. This architectural pattern has been widely adopted, with 7,498+ citations.

## Key Properties

- **Frozen components**: Both image encoder (ViT) and LLM (OPT/FlanT5) remain completely frozen during training
- **Q-Former bridge**: 12-layer Transformer with 32 learnable queries extracts task-relevant visual features via cross-attention
- **Two-stage pre-training**: Stage 1 (representation alignment with frozen encoder), Stage 2 (generative connection to frozen LLM)
- **Three objectives**: Image-Text Contrastive (ITC), Image-Text Matching (ITM), Image-grounded Text Generation (ITG) — same architecture, different attention masks
- **Modular**: Image encoders and LLMs can be independently swapped and upgraded
- **54× parameter efficiency**: ~188M trainable parameters vs Flamingo's 10.2B

## Related Terms

- **[Q-Former](term_q_former.md)**: The core architectural innovation — lightweight Querying Transformer that bridges modalities
- **[Contrastive Learning](term_contrastive_learning.md)**: ITC pre-training objective for representation alignment
- **[Transformer](term_transformer.md)**: Q-Former is a Transformer encoder with cross-attention
- **[BERT](term_bert.md)**: Q-Former initialized from BERT-base
- **[Foundation Model](term_foundation_model.md)**: BLIP-2 leverages frozen foundation models
- **[Phi](term_phi.md)**: SOPA uses Phi-3 as the frozen LLM in a BLIP-2-inspired architecture
- **[Zero-Shot Learning](term_zero_shot_learning.md)**: Emergent zero-shot VQA and instruction following

## References

### Vault Sources

- [BLIP-2 Literature Note](../papers/lit_li2023blip2.md) — Full paper digest with section notes
- [BLIP-2 Review](../papers/review_li2023blip2.md) — OpenReview-style evaluation
- [SOPA LLM](../../areas/models/model_sopa_llm.md) — Production adaptation for abuse prevention

### External Sources

- [Li et al. (2023). "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models." ICML](https://arxiv.org/abs/2301.12597)
- [Hugging Face: BLIP-2](https://huggingface.co/docs/transformers/model_doc/blip-2)

### Related Code Repos

- [SOPA-LLM](../../areas/code_repos/repo_sopa_llm.md) — SOP-Aware multi-modal LLM implementation
