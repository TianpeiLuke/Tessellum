---
tags:
  - resource
  - terminology
  - machine_learning
  - deep_learning
  - computer_vision
  - multimodal
keywords:
  - VLM
  - Vision Language Model
  - multimodal
  - image understanding
  - CLIP
  - ViT
  - visual question answering
  - document understanding
topics:
  - buyer risk prevention
  - machine learning
  - computer vision
  - multimodal AI
  - deep learning
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/WW-CT-ML-Foundational-Capabilities/Computer_Vision_Working_Group/AMLC2025_Workshop_of_CV_for_Customer_Trust/
---

# VLM - Vision Language Model

## Definition

**VLM** stands for **Vision Language Model**. VLMs are multimodal AI models that can process both images and text, enabling them to understand visual content using natural language. Modern VLMs (2023+) typically use a pre-trained Vision Transformer (ViT) backbone to process images, fusing image embeddings with text embeddings at various stages of a transformer architecture. At Amazon/BRP, VLMs are deployed for document understanding (customer evidence verification), tamper detection, fraud detection, and return abuse prevention where visual signals from product images or uploaded documents are critical for decision-making.

**Key Function**: Enable AI systems to comprehend and reason about visual content using natural language, supporting tasks like visual question answering (VQA), document information extraction, image captioning, and fraud/abuse detection from images.

## Full Name

**Vision Language Model**

**Synonyms & Related Terms**:
- **Multimodal LLM**: Language model capable of processing multiple modalities
- **Vision-Language Pre-training (VLP)**: Training paradigm for VLMs
- **Visual Question Answering (VQA)**: Key VLM task
- **Document VLM**: VLM specialized for document understanding
- **MLLM (Multimodal Large Language Model)**: Larger VLM variants

## Key Highlights

**Architecture**: VLMs combine a Vision Encoder (typically ViT/CLIP) with a Language Model backbone through a fusion layer (cross-attention, linear projector, or Q-Former). Three main fusion strategies exist -- late fusion (CLIP), middle fusion (PaLI), and early fusion (Fuyu) -- with popular model families including CLIP, BLIP-2, LLaVA, Qwen2-VL, GPT-4V, and Claude 3. For detailed architecture diagrams and component breakdowns, see [VLM Architecture and How VLMs Work](../analysis_thoughts/thought_vlm_architecture.md).

**BRP Applications**: VLMs are deployed across Amazon/BRP for document verification (Document VLM achieving 94% accuracy vs 51% OCR), return abuse prevention (Guardian), tamper detection, book fraud detection (Phoenix Shield), and CAPTCHA defense (MASN). Research applications include Last Mile delivery and curriculum learning. For full details on each application, see [VLM Applications at Amazon/BRP](../analysis_thoughts/thought_vlm_brp_applications.md).

**Implementation and Evaluation**: Fine-tuning VLMs (e.g., Qwen2-VL) for fraud detection uses reference-aware prompting and two-stage pipelines for document processing. VLMs outperform OCR+LLM pipelines for complex documents while facing challenges around inference latency, hallucination, privacy, and adversarial robustness. See [VLM Technical Implementation](../policy_sops/sop_vlm_implementation.md) and [VLM Evaluation and Challenges](../analysis_thoughts/thought_vlm_evaluation.md) for details.

## Related Terms

### Architecture Components
- **[ViT](term_vit.md)** - Vision Transformer (image encoder)
- **[Transformer](term_transformer.md)** - Foundational architecture
- **[CLIP](term_clip.md)** - Contrastive Language-Image Pre-training

### Language Models
- **[LLM](term_llm.md)** - Large Language Model (text-only)
- **[BERT](term_bert.md)** - Encoder-only transformer for text

### BRP Applications
- **[Guardian](term_guardian.md)** - Multimodal LLM for return abuse (if exists)
- **[DeepCARE](term_deepcare.md)** - Investigation automation
- **[AutoSignality](term_autosignality.md)** - LLM-based fraud automation

### Related Concepts
- **[OCR](term_ocr.md)** - Optical Character Recognition
- **[Multimodal](term_multimodal.md)** - Multiple input modalities
- **[Embedding](term_embedding.md)** - Dense vector representations (image/text fusion)

## See Also

- [VLM Architecture and How VLMs Work](../analysis_thoughts/thought_vlm_architecture.md) -- Architecture overview, fusion strategies, key VLM families, and core components (vision encoder, projector, language model backbone)
- [VLM Applications at Amazon/BRP](../analysis_thoughts/thought_vlm_brp_applications.md) -- Production applications (Document VLM, Guardian, tamper detection, Phoenix Shield, CAPTCHA defense) and research applications (Last Mile, curriculum learning)
- [VLM Technical Implementation](../policy_sops/sop_vlm_implementation.md) -- Fine-tuning code examples, prompting strategies (simple, reference-aware, chain-of-thought), and two-stage document processing pipeline
- [VLM Evaluation and Challenges](../analysis_thoughts/thought_vlm_evaluation.md) -- Comparison with OCR+LLM and CV+Rules approaches, VLM selection guidance at BRP, and key challenges (latency, hallucination, privacy, adversarial robustness)

## References

### Launch Announcements
- [PROPHET 2.0 Multi-Modal AI Agent for Impersonation Phishing (December 2025)](../../archives/launch_announcements/2025-12-15_launch-announcement-prophet-20-multi-modal-ai-agent-for-impersonation-phishing.md) - Agentic AI system using multimodal (text + visual) analysis to detect phishing websites impersonating Amazon

### Amazon Internal
- **Document VLM Wiki**: https://w.amazon.com/bin/view/Cosine/DocumentGPT/
- **Guardian Project**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/Shengjie/Guardian/
- **VLM Last Mile**: https://w.amazon.com/bin/view/Last_Mile_ML_Science/Projects/VLM/
- **CAPTCHA Mitigation**: https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/BotMitigationML/CAPTCHAInternProject2024/
- **CV4CT Workshop AMLC 2025**: https://w.amazon.com/bin/view/WW-CT-ML-Foundational-Capabilities/Computer_Vision_Working_Group/AMLC2025_Workshop_of_CV_for_Customer_Trust/
- **Efficient VLM Tutorial AMLC 2025**: https://w.amazon.com/bin/view/AMLC-2025-Tutorial-Efficient-Vision-Language-Models-Architectures-Training-and-Inference-Optimization/

### External Resources
- **CLIP Paper**: [Learning Transferable Visual Models](https://arxiv.org/abs/2103.00020)
- **LLaVA Paper**: [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485)
- **Qwen2-VL**: https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct

## Summary

**VLM Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Vision Language Model |
| **Architecture** | Vision encoder + Language model + Fusion |
| **Key Components** | ViT, Cross-attention/Projector, Transformer LLM |
| **Popular Models** | CLIP, BLIP-2, LLaVA, Qwen2-VL, GPT-4V, Claude 3 |
| **BRP Applications** | Document VLM (CSSW), Guardian, Tamper Detection, CAPTCHA Defense |
| **Key Strength** | Understand images with natural language reasoning |
| **Best For** | Document verification, visual fraud detection, multimodal abuse |
| **Deployment** | CoSS Document VLM in production (94% accuracy) |

**Key Insight**: VLMs represent the **convergence of computer vision and NLP**, enabling AI systems to reason about visual content using natural language. At BRP, VLMs address the critical gap in abuse detection where **visual evidence** (customer documents, product images, appeal evidence) is central to fraud/abuse decisions. The Document VLM (94% accuracy vs 51% OCR) demonstrates how VLMs dramatically improve document verification in Customer Self-Service Workflow, while Guardian shows how VLMs can **read SOPs directly from images** to automate return abuse decisions. As customers increasingly submit images as evidence (receipts, photos, documents), VLMs provide the multimodal understanding necessary for accurate, scalable abuse prevention. The AMLC 2025 CV4CT Workshop highlights VLM adoption across Customer Trust for tamper detection, book fraud, and multimodal product analysis--signaling VLMs as a growing foundation technology for visual fraud detection at Amazon.

---

**Last Updated**: March 15, 2026
**Status**: Active - emerging technology for visual fraud/abuse detection
