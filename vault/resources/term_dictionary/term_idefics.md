---
tags:
  - resource
  - terminology
  - machine_learning
  - vlm
  - foundation_model
  - open_source
keywords:
  - IDEFICS
  - IDEFICS-v2
  - vision language model
  - HuggingFace
  - Flamingo
  - open-source VLM
  - interleaved cross-attention
  - Laurencon 2024
topics:
  - foundation models
  - vision language models
  - open-source AI
language: markdown
date of note: 2026-04-03
status: active
building_block: concept
---

# IDEFICS (Image-aware Decoder Enhanced à la Flamingo with Interleaved Cross-attentionS)

## Definition

**IDEFICS** is an open-source vision-language model family from HuggingFace, designed as an accessible reproduction of DeepMind's closed-source Flamingo model. It processes arbitrary sequences of interleaved images and text, producing text outputs for visual question answering, image captioning, multi-image reasoning, and story generation.

**IDEFICS-v2** (8B parameters, Apache 2.0 license) improved upon the original 80B model with a more efficient architecture, better training recipes, enhanced OCR capabilities, and significantly reduced parameter count while maintaining competitive performance. The key architectural insight from the "What matters when building VLMs?" paper was that careful data curation and training methodology matter more than raw model size.

## Key Properties

- **Interleaved cross-attention**: Processes mixed sequences of images and text — images are injected into the language model via cross-attention layers at regular intervals
- **Two variants**: IDEFICS-1 (80B/9B parameters) and IDEFICS-v2 (8B parameters, more efficient)
- **Open license**: Apache 2.0 — enabling fine-tuning, commercial use, and research
- **Few-shot learning**: Strong in-context learning from interleaved image-text examples
- **OCR capabilities**: Enhanced in v2 for document understanding and text extraction from images

## Amazon Context

IDEFICS-v2 was the **first-generation VLM backbone** for VISTA (2024). The IML team fine-tuned it on curated in-house e-commerce datasets (200k annotated images with captions), achieving results published at **NAACL'25** (Tier-1 NLP conference). It was subsequently replaced by Qwen2.5-VL in 2025 Q2 for better performance (+16% accuracy, -58% hallucination rate), but the NAACL publication established VISTA's scientific credibility.

## Related Terms

- **[Qwen](term_qwen.md)**: Successor foundation model in VISTA — Qwen2.5-VL replaced IDEFICS-v2
- **[VLM](term_vlm.md)**: Vision Language Model — the model category
- **[LoRA](term_lora.md)**: Low-Rank Adaptation — used for task-specific fine-tuning on top of IDEFICS-v2
- **[Fine-Tuning](term_fine_tuning.md)**: Training methodology used to adapt IDEFICS-v2 for VISTA

## References

### Vault Sources
- [Model: VISTA VLM — History](../../areas/models/model_vista_vlm_history.md) — IDEFICS-v2 as Gen-1 backbone
- [VISTA Science Capabilities](../../projects/vista/vista_science_capabilities.md) — Training details

### External Sources
- [Laurençon et al. (2024). "What matters when building vision-language models?" HuggingFace](https://huggingface.co/blog/idefics2)
- [IDEFICS-v2 Model Card — HuggingFace](https://huggingface.co/HuggingFaceM4/idefics2-8b)
