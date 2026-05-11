---
tags:
  - resource
  - terminology
  - multimodal
  - vision_language
  - contrastive_learning
  - zero_shot
keywords:
  - CLIP
  - Contrastive Language-Image Pre-training
  - dual encoder
  - zero-shot transfer
  - vision-language
  - OpenAI
  - natural language supervision
  - image classification
  - ViT
  - cosine similarity
topics:
  - Multimodal Learning
  - Computer Vision
  - Contrastive Learning
  - Vision-Language Models
language: markdown
date of note: 2026-03-31
status: active
building_block: concept
---

# CLIP (Contrastive Language-Image Pre-training)

## Definition

**CLIP (Contrastive Language-Image Pre-training)** is a multimodal vision-language model developed by OpenAI (Radford et al., 2021) that learns visual representations from natural language supervision. CLIP trains a dual-encoder architecture — an image encoder (ViT or ResNet) and a text encoder (Transformer) — on 400 million internet image-text pairs using a contrastive objective that aligns matching image-text pairs in a shared embedding space. This enables **zero-shot transfer** to arbitrary vision tasks: at inference, class labels are converted to text prompts ("a photo of a {class}"), and classification is performed by finding the prompt most similar to the image embedding.

CLIP matches supervised ResNet-50 on ImageNet (76.2%) without any ImageNet training data, demonstrates dramatically superior robustness to distribution shift, and has become the standard frozen vision encoder for subsequent multimodal AI systems. With 45,741+ citations, CLIP is one of the most influential ML papers of the decade.

## Key Properties

- **Natural language as supervision**: Text descriptions replace fixed categorical labels, enabling open-vocabulary visual understanding
- **Dual-encoder contrastive learning**: Symmetric cross-entropy loss over cosine similarities in a batch (batch size 32,768)
- **Zero-shot transfer**: Text prompts serve as classifiers — "a photo of a {class}" enables classification on any task without task-specific training
- **Distribution shift robustness**: Zero-shot CLIP degrades much less than supervised models on shifted datasets (+36% on ImageNet-Sketch, +75% on ImageNet-A)
- **ViT preferred**: Vision Transformer encoders (ViT-B/32, ViT-L/14) consistently outperform ResNet variants at equivalent compute
- **Frozen backbone standard**: CLIP's ViT-L/14 (and EVA-CLIP's ViT-G/14) became the default frozen image encoder for BLIP-2, LLaVA, Stable Diffusion, and DALL-E 2
- **Prompt engineering**: Prompt design significantly affects zero-shot performance; prompt ensembling further improves results

## Architecture

| Component | Details |
|-----------|---------|
| **Image encoder** | ViT-L/14 (304M params, preferred) or ResNet variants |
| **Text encoder** | 12-layer Transformer, 512-dim, 8 heads, BPE tokenization |
| **Projection** | Linear projection to shared embedding space |
| **Training objective** | Symmetric contrastive loss over cosine similarities |
| **Training data** | WebImageText (WIT): 400M image-text pairs from internet |
| **Batch size** | 32,768 (critical for contrastive learning quality) |

## Applications

| Domain | Application | Example |
|--------|-------------|---------|
| **Zero-Shot Classification** | Image classification without task-specific training | 76.2% ImageNet accuracy with no labeled data |
| **Image-Text Retrieval** | Finding images matching text queries or vice versa | COCO/Flickr30k retrieval benchmarks |
| **Multimodal Foundation** | Frozen vision backbone for vision-language systems | [BLIP-2](term_blip2.md) uses frozen CLIP ViT as image encoder |
| **Image Generation** | Guiding text-to-image generation models | DALL-E 2 uses CLIP embeddings for text guidance |
| **Abuse Prevention** | Upstream vision encoder in the CLIP → BLIP-2 → SOPA lineage | [SOPA](../../areas/models/model_sopa_llm.md) inherits CLIP's representation quality via BLIP-2 |

## Related Terms

- **[BLIP-2](term_blip2.md)**: Uses CLIP's frozen ViT as its image encoder; Q-Former bridges CLIP to LLMs
- **[Q-Former](term_q_former.md)**: Bridges CLIP's visual representations to frozen LLMs via learnable queries
- **[CCA](term_cca.md)**: CLIP's contrastive objective is a nonlinear, stochastic generalization of Canonical Correlation Analysis — both maximize correspondence between two modalities
- **[Contrastive Learning](term_contrastive_learning.md)**: CLIP's core training objective — aligning positive pairs while pushing negatives apart
- **[Dimensionality Reduction](term_dimensionality_reduction.md)**: CLIP projects images and text into a shared low-dimensional embedding space — a learned cross-modal dimensionality reduction
- **[Zero-Shot Learning](term_zero_shot_learning.md)**: CLIP's key capability — classification without task-specific training
- **[Transformer](term_transformer.md)**: Both encoders use Transformer architecture (ViT for images, standard Transformer for text)
- **[Foundation Model](term_foundation_model.md)**: CLIP's frozen encoder serves as a foundation for downstream multimodal systems
- **[Phi](term_phi.md)**: Phi-3-mini serves as the frozen LLM in SOPA, which inherits CLIP's vision representations via BLIP-2
- **[Scaling Law](term_scaling_law.md)**: CLIP shows smooth compute-performance scaling across ViT and ResNet families

## References

### Vault Sources

- [CLIP Literature Note](../papers/lit_radford2021clip.md) — Full paper digest with section notes
- [CLIP Review](../papers/review_radford2021clip.md) — OpenReview-style evaluation (Overall 9/10)
- [BLIP-2 Literature Note](../papers/lit_li2023blip2.md) — Builds directly on CLIP
- [SOPA LLM](../../areas/models/model_sopa_llm.md) — End of the CLIP → BLIP-2 → SOPA lineage

### External Sources

- [Radford et al. (2021). "Learning Transferable Visual Models From Natural Language Supervision." ICML](https://arxiv.org/abs/2103.00020) — Original CLIP paper (45,741 citations)
- [OpenAI: CLIP](https://openai.com/index/clip/) — Official announcement
- [Hugging Face: CLIP](https://huggingface.co/docs/transformers/model_doc/clip) — Implementation and pre-trained models
- [GitHub: openai/CLIP](https://github.com/openai/CLIP) — Open-source code and weights
