---
tags:
  - resource
  - terminology
  - machine_learning
  - vlm
  - foundation_model
  - llm
keywords:
  - Qwen
  - Qwen2.5-VL
  - QwenVL
  - vision language model
  - Alibaba
  - multimodal
  - native resolution
  - dynamic frame sampling
topics:
  - foundation models
  - vision language models
  - multimodal AI
language: markdown
date of note: 2026-04-03
status: active
building_block: concept
---

# Qwen (QwenVL / Qwen2.5-VL)

## Definition

**Qwen** is Alibaba's family of large language models. **Qwen2.5-VL** is the vision-language variant that combines the language capabilities of Qwen 2.5 with a new Vision Transformer encoder, enabling processing of images, videos, and text in a unified architecture. Available in 3B, 7B, and 72B parameter sizes under permissive licenses (Apache 2.0), Qwen2.5-VL processes images at native resolution (no fixed-size resizing), uses dynamic frame sampling for videos, and integrates absolute time encoding for temporal understanding.

Key capabilities include visual question answering, OCR (including handwritten text and multilingual signage), document/chart parsing, object localization with bounding boxes, video understanding (1+ hour videos with second-level precision), and agent-based interaction with GUIs.

## Key Properties

- **Native resolution processing**: Images are processed at their original resolution with dynamic token counts — larger images get more tokens, preserving detail
- **Multi-scale variants**: 3B (edge/mobile), 7B (balanced), 72B (maximum capability) — all share the same architecture
- **Video understanding**: Dynamic frame sampling with absolute time encoding enables precise temporal localization
- **Agent capabilities**: Can interact with computer/phone GUIs, parse structured documents, and execute multi-step visual reasoning
- **Open weights**: Released under Apache 2.0 license, enabling fine-tuning and commercial use

## Amazon Context

**Qwen2.5-VL** is the current foundation model for VISTA's VLM track, replacing IDEFICS-v2 in 2025 Q2. The migration delivered 16% accuracy improvement (73.8% → 85.6%) and 58% hallucination reduction (24.2% → 10.0%) at <$1,000 training cost and 2 weeks of scientist bandwidth. VISTA fine-tunes Qwen2.5-VL with task-specific LoRA adapters for damage detection, product matching, expiry validation, and other CV tasks. The 2026 roadmap plans evaluation of multiple QwenVL variants (1B, 3B, 7B) with quantization and compression for latency optimization.

## Related Terms

- **[VLM](term_vlm.md)**: Vision Language Model — the model category Qwen2.5-VL belongs to
- **[IDEFICS](term_idefics.md)**: Previous VISTA foundation model, replaced by Qwen2.5-VL
- **[LoRA](term_lora.md)**: Low-Rank Adaptation — used to fine-tune Qwen2.5-VL for VISTA tasks
- **[ViT](term_vit.md)**: Vision Transformer — the vision encoder architecture
- **[Hallucination](term_hallucination.md)**: Model hallucination — reduced 58% by Qwen2.5-VL migration

## References

### Vault Sources
- [Model: VISTA VLM](../../areas/models/model_vista_vlm.md) — Uses Qwen2.5-VL as foundation model
- [VISTA Science Capabilities](../../projects/vista/vista_science_capabilities.md) — Architecture migration details

### External Sources
- [Bai et al. (2025). "Qwen2.5-VL Technical Report." Alibaba Group](https://qwen-ai.com/qwen-vision/)
- [Qwen2.5-VL Model Card — HuggingFace](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)
