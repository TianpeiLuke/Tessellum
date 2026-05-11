---
tags:
  - resource
  - literature_note
  - knowledge_distillation
  - model_compression
  - nlp
keywords:
  - DistilBERT
  - knowledge distillation
  - BERT
  - model compression
  - pre-training distillation
  - triple loss
  - softmax temperature
  - student-teacher
topics:
  - Knowledge Distillation
  - Model Compression
  - NLP
domain: "Knowledge Distillation"
language: markdown
date of note: 2026-03-16
paper_title: "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter"
authors:
  - Victor Sanh
  - Lysandre Debut
  - Julien Chaumond
  - Thomas Wolf
year: 2019
source: "arXiv:1910.01108"
venue: "NeurIPS 2019 Workshop (EMC²)"
arXiv: "1910.01108"
semantic_scholar_id: "a54b56af24bb4873ed0163b77df63b92bd018ddc"
zotero_key: "MEM9Q6XX"
paper_id: sanh2019distilbert
paper_notes:
  - paper_sanh2019distilbert_intro.md
  - paper_sanh2019distilbert_contrib.md
  - paper_sanh2019distilbert_model.md
  - paper_sanh2019distilbert_exp_design.md
  - paper_sanh2019distilbert_exp_result.md
status: active
building_block: hypothesis
---

# DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter |
| **Authors** | Victor Sanh, Lysandre Debut, Julien Chaumond, Thomas Wolf |
| **Year** | 2019 |
| **Venue** | NeurIPS 2019 Workshop (EMC²) |
| **arXiv** | [1910.01108](https://arxiv.org/abs/1910.01108) |
| **Semantic Scholar** | [a54b56a...](https://www.semanticscholar.org/paper/a54b56af24bb4873ed0163b77df63b92bd018ddc) |
| **Zotero** | MEM9Q6XX |
| **Citations** | ~9,294 |
| **Code** | [huggingface/transformers](https://github.com/huggingface/transformers) |

## Abstract

Large-scale pre-trained models have become standard in NLP. The authors present DistilBERT, a method to pre-train a smaller general-purpose language representation model using knowledge distillation. DistilBERT reduces the size of a BERT model by 40% (66M vs 110M parameters), while retaining 97% of its language understanding capabilities (GLUE macro-score 77.0 vs 79.5) and being 60% faster. The approach combines language modeling, distillation, and cosine-distance losses in a triple loss framework applied during pre-training.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_sanh2019distilbert_intro](paper_sanh2019distilbert_intro.md) | Environmental/computational cost motivation; gap in pre-training distillation; task-agnostic compression need |
| **Contribution** | [paper_sanh2019distilbert_contrib](paper_sanh2019distilbert_contrib.md) | Triple loss distillation during pre-training; teacher initialization; 40% smaller / 97% performance / 60% faster |
| **Model** | [paper_sanh2019distilbert_model](paper_sanh2019distilbert_model.md) | 6-layer student; triple loss (Lce + Lmlm + Lcos); softmax-temperature; teacher weight initialization |
| **Experiment Design** | [paper_sanh2019distilbert_exp_design](paper_sanh2019distilbert_exp_design.md) | GLUE benchmark, SQuAD v1.1, IMDb; BERT-base and ELMo baselines; 8×V100 training |
| **Experiment Results** | [paper_sanh2019distilbert_exp_result](paper_sanh2019distilbert_exp_result.md) | 97% GLUE retention; ablation shows all losses matter; teacher init worth +3.69 points; on-device 71% faster |
| **Review** | [review_sanh2019distilbert](review_sanh2019distilbert.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 9 questions (4 review lenses applied) |

## Summary

- **Background**: Large pre-trained language models like BERT achieve state-of-the-art NLP performance but require significant compute and memory, limiting deployment on edge devices and raising environmental concerns. Prior distillation work focused on task-specific compression, leaving a gap in general-purpose pre-training distillation. <!-- VERIFY -->
- **Contribution**: DistilBERT introduces a triple loss framework (distillation cross-entropy Lce, masked language modeling Lmlm, cosine embedding Lcos) applied during pre-training to compress BERT-base into a 6-layer student model. The student is initialized by taking every other layer from the teacher, leveraging shared architecture dimensions. <!-- VERIFY -->
- **Model**: The student architecture halves BERT's depth (6 vs 12 layers) while keeping hidden size (768), attention heads (12), and FFN dimension (3072) identical. Training uses softmax-temperature to produce soft probability distributions from the teacher. Token-type embeddings and pooler are removed; next sentence prediction is dropped. <!-- VERIFY -->
- **Results**: DistilBERT retains 97% of BERT-base's GLUE macro-score (77.0 vs 79.5) with 40% fewer parameters (66M vs 110M) and 60% faster inference. Ablation shows teacher initialization is the most impactful component (+3.69 points), followed by distillation loss. On an iPhone 7 Plus, DistilBERT achieves 71% speedup over BERT. <!-- VERIFY -->

## Relevance to Our Work

- **[Knowledge Distillation](../term_dictionary/term_knowledge_distillation.md)**: DistilBERT is the seminal application of knowledge distillation to pre-trained language model compression — the canonical example of the technique
- **[BERT](../term_dictionary/term_bert.md)**: DistilBERT's teacher model; demonstrates that BERT's representations are compressible via distillation
- **[Transformer](../term_dictionary/term_transformer.md)**: DistilBERT preserves the Transformer encoder architecture while halving depth
- **[Quantization](../term_dictionary/term_quantization.md)**: Complementary compression approach — the paper notes DistilBERT's 207MB model "could be further reduced with quantization"
- **[Scaling Law](../term_dictionary/term_scaling_law.md)**: DistilBERT addresses the practical consequence of scaling laws — larger models perform better but need compression for deployment

## Related Documentation

### Paper Notes
- [Introduction](paper_sanh2019distilbert_intro.md)
- [Contribution](paper_sanh2019distilbert_contrib.md)
- [Model](paper_sanh2019distilbert_model.md)
- [Experiment Design](paper_sanh2019distilbert_exp_design.md)
- [Experiment Results](paper_sanh2019distilbert_exp_result.md)

### Related Vault Notes
- [Knowledge Distillation](../term_dictionary/term_knowledge_distillation.md) — the core technique applied in this paper
- [BERT](../term_dictionary/term_bert.md) — the teacher model being compressed
- [Transformer](../term_dictionary/term_transformer.md) — base architecture for both teacher and student
- [Quantization](../term_dictionary/term_quantization.md) — complementary model compression via precision reduction
- [Scaling Law](../term_dictionary/term_scaling_law.md) — motivation: larger models need compression for deployment

### Related Literature
- Devlin et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers" — [lit_devlin2019bert](lit_devlin2019bert.md) — the teacher model
- Dettmers et al. (2022). "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale" — [lit_dettmers2022llm](lit_dettmers2022llm.md) — complementary compression via quantization
- Hu et al. (2021). "LoRA: Low-Rank Adaptation of Large Language Models" — [lit_hu2021lora](lit_hu2021lora.md) — alternative parameter-efficient approach
