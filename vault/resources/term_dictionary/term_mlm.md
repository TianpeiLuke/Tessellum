---
tags:
  - resource
  - terminology
  - nlp
  - self_supervised_learning
  - pre_training
keywords:
  - masked language model
  - MLM
  - BERT
  - cloze task
  - pre-training
  - bidirectional
  - masking strategy
  - SpanBERT
  - RoBERTa
  - ELECTRA
topics:
  - Natural Language Processing
  - Self-Supervised Learning
  - Pre-training
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Masked Language Model (MLM)

## Definition

**Masked Language Model (MLM)** is a self-supervised pre-training objective where a fraction of input tokens are randomly masked (replaced with a special `[MASK]` token) and the model is trained to predict the original tokens using **full bidirectional context**. Introduced in BERT (Devlin et al., 2019), MLM is a computational implementation of the Cloze task (Taylor, 1953) applied to Transformer pre-training. Unlike autoregressive language modeling (which predicts tokens left-to-right), MLM enables each masked token to attend to both left and right context in every layer, producing deep bidirectional representations.

## Full Name

**Masked Language Model (MLM)**

**Also Known As**: Cloze-style pre-training, masked token prediction, denoising objective

## Mathematical Formulation

Given an input sequence $\mathbf{x} = (x_1, x_2, \ldots, x_n)$, MLM selects a subset of positions $\mathcal{M} \subset \{1, \ldots, n\}$ for masking. The training objective minimizes cross-entropy loss over masked positions only:

$$\mathcal{L}_{\text{MLM}}(\theta) = -\sum_{i \in \mathcal{M}} \log P_\theta(x_i \mid \hat{\mathbf{x}})$$

where $\hat{\mathbf{x}}$ is the corrupted input with masked positions replaced. Crucially, each masked token is predicted **independently** of other masked tokens — an assumption XLNet (Yang et al., 2019) identified as a structural limitation.

## BERT's Masking Strategy

BERT masks **15%** of input tokens per sequence. Of the selected tokens:

| Treatment | Proportion | Rationale |
|-----------|-----------|-----------|
| Replace with `[MASK]` | 80% | Provides the primary training signal |
| Replace with random token | 10% | Forces the model to maintain representations for all tokens, not just masked ones |
| Keep unchanged | 10% | Biases the model toward the actual observed distribution, reducing pre-train/fine-tune mismatch |

**Why 15%?** A balance between training signal density (more masking = more gradient per step) and prediction difficulty (more masking = less context available). The rate was chosen empirically; later work (Wettig et al., 2023) found that rates up to 40% can work with appropriate modifications.

**Why 80/10/10?** If 100% were `[MASK]`, the model would only learn to predict in the presence of a token that never appears during fine-tuning. The 10% random + 10% unchanged cases ensure the encoder builds useful representations for all token positions, not just masked ones.

## Key Variants and Extensions

| Variant | Paper | Year | Innovation | Impact |
|---------|-------|------|------------|--------|
| **Whole Word Masking** | Cui et al. | 2019 | Masks all WordPiece subword tokens of a word together | Prevents trivial prediction from adjacent subwords |
| **RoBERTa** | Liu et al. | 2019 | Dynamic masking (new mask each epoch) + no NSP + more data/compute | Showed BERT was undertrained; dynamic masking > static |
| **SpanBERT** | Joshi et al. | 2020 | Contiguous span masking (geometric distribution) + Span Boundary Objective | Better for span extraction tasks (QA, coreference) |
| **ALBERT** | Lan et al. | 2020 | Replaces NSP with Sentence Order Prediction (SOP) | Harder, topic-independent coherence task |
| **ELECTRA** | Clark et al. | 2020 | Replaced Token Detection: train a generator to produce replacements, train a discriminator to detect them | Training signal from **100%** of tokens (not 15%), ~4x more sample-efficient |
| **XLM / mBERT** | Lample & Conneau | 2019 | Cross-lingual MLM on concatenated multilingual text + Translation Language Modeling (TLM) | Enables cross-lingual transfer |
| **XLNet** | Yang et al. | 2019 | Permutation Language Modeling: autoregressive over all permutations of factorization order | Removes independence assumption; no `[MASK]` token mismatch |

## MLM vs. Autoregressive Language Modeling

| Dimension | MLM (BERT-style) | Autoregressive LM (GPT-style) |
|-----------|-------------------|-------------------------------|
| **Context** | Bidirectional (full context at every layer) | Unidirectional (left-to-right only) |
| **Training signal** | 15% of tokens per input | 100% of tokens per input |
| **Generation** | Cannot generate text natively | Natural text generation |
| **Pre-train/fine-tune gap** | `[MASK]` token absent at inference | No gap |
| **Best for** | Classification, NER, QA (understanding) | Text generation, dialogue, reasoning |
| **Independence assumption** | Masked tokens predicted independently | Autoregressive factorization is exact |

## Connection to the Cloze Task

The Cloze procedure (Taylor, 1953) is a reading comprehension test where words are deleted from a passage and the reader fills them in. MLM is a large-scale computational implementation of this idea, substituting gradient descent for human judgment. The key difference: Cloze tests typically remove every 5th word (~20%), while BERT uses 15%. Taylor's insight — that fill-in-the-blank tests measure contextual understanding — directly motivates why MLM produces strong bidirectional representations.

## Limitations

1. **Pre-train/fine-tune mismatch**: The `[MASK]` token is an artificial construct that never appears during fine-tuning, creating a distributional shift. The 80/10/10 split mitigates but does not eliminate this.
2. **Low signal density**: Only 15% of tokens produce a gradient per training step (vs. 100% for autoregressive LMs), requiring more compute to converge.
3. **Independence assumption**: Masked tokens are predicted independently of each other, ignoring their joint distribution. For example, masking "New" and "York" independently may produce valid individual predictions but incoherent joint predictions.
4. **Not generative**: Encoder-only MLM models cannot generate text autoregressively, limiting their applicability to understanding tasks.

## Applications to Our Work

- **BSM-BERT models** ([RnR BSM BERT](../../areas/models/model_rnr_bsm_bert.md), [AtoZ BSM BERT](../../areas/models/model_atoz_bsm_bert.md)) use the MLM-pre-trained BERT encoder as their backbone, fine-tuning the `[CLS]` representation for buyer-seller message abuse classification.
- Domain-specific continued pre-training with MLM on abuse-related text (customer contacts, seller messages) could improve representations for abuse detection.

## Related Terms

### Core Concepts
- [Self-Supervised Learning](term_ssl.md) — MLM is the canonical SSL objective for NLP
- [BERT](term_bert.md) — The model that introduced MLM for Transformer pre-training
- [Transformer](term_transformer.md) — Architecture that MLM pre-trains

### Extensions and Alternatives
- [LLM](term_llm.md) — Large Language Models typically use autoregressive objectives (GPT-style), not MLM
- [Contrastive Learning](term_contrastive_learning.md) — Alternative SSL objective; sometimes combined with MLM
- [Fine-Tuning](term_fine_tuning.md) — The downstream adaptation step after MLM pre-training
- [Masked Diffusion](term_masked_diffusion.md) — Extends MLM's masking to multi-step iterative generation; unifies masking with diffusion framework

### Production Models
- [SBERT](term_sbert.md) — Extends MLM-pre-trained BERT for sentence embeddings
- [CrossBERT](term_crossbert.md) — Cross-marketplace BERT model built on MLM pre-training

## References

- Devlin, J. et al. (2019). [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](../papers/lit_devlin2019bert.md). NAACL.
- Taylor, W.L. (1953). Cloze procedure: A new tool for measuring readability. *Journalism Quarterly*.
- Liu, Y. et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach. arXiv:1907.11692.
- Clark, K. et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators. ICLR.
- Joshi, M. et al. (2020). SpanBERT: Improving Pre-training by Representing and Predicting Spans. TACL.
- Yang, Z. et al. (2019). XLNet: Generalized Autoregressive Pretraining for Language Understanding. NeurIPS.
- Wettig, A. et al. (2023). Should You Mask 15 Percent in Masked Language Modeling? EACL.
