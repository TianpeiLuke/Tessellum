---
tags:
  - resource
  - terminology
  - uncertainty_quantification
  - llm
  - probing
  - hallucination_detection
keywords:
  - semantic entropy probes
  - SEP
  - linear probes
  - hidden states
  - hallucination detection
  - uncertainty estimation
  - single-pass inference
  - logistic regression
  - out-of-distribution generalization
topics:
  - Uncertainty Quantification
  - Large Language Models
  - Representation Learning
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Semantic Entropy Probes (SEP)

## Definition

**Semantic Entropy Probes (SEP)** are lightweight linear classifiers (logistic regression) trained on LLM hidden states to predict [semantic entropy](term_semantic_entropy.md) in a **single forward pass**, eliminating the need for multiple generations and [NLI](term_nli.md) clustering at inference time. The probes are trained on hidden-state/SE label pairs: the supervisory signal comes from computing full semantic entropy on training examples, then binarizing into high/low uncertainty classes.

**Full Name**: Semantic Entropy Probes

**Key insight**: LLM hidden states already encode semantic uncertainty information. A simple L2-regularized logistic regression on mid-to-late layer activations can predict whether the model's output will be semantically uncertain — without generating multiple responses.

## How It Works

### Training Phase (offline, one-time)

1. **Generate**: For each training query, sample M=10 responses at T=1.0
2. **Compute SE**: Cluster responses via [bidirectional entailment](term_bidirectional_entailment.md), compute discrete semantic entropy
3. **Binarize**: Split SE scores into high/low uncertainty using optimal threshold (minimizes within-class variance)
4. **Extract features**: Run a single greedy generation; extract hidden states from a chosen token position and layer
5. **Train probe**: Fit L2-regularized logistic regression on hidden states → binary SE label

Training requires only ~2,000 examples for short-form QA, ~1,000 for long-form. CPU-only training with scikit-learn.

### Inference Phase (online, per-query)

1. Run a **single forward pass** (greedy generation or input encoding only)
2. Extract hidden state from the chosen token position
3. Apply the trained probe → uncertainty prediction

**No multiple generations. No NLI calls. Near-zero overhead.**

### Token Positions

| Position | Name | Requires | Performance |
|----------|------|----------|-------------|
| **SLT** | Second-Last Token | Full response generation | Best AUROC |
| **TBG** | Token-Before-Generating | Input encoding only | Slightly lower AUROC, but enables pre-generation uncertainty estimation |

TBG is the most practically interesting variant: it enables uncertainty estimation *before* generating any response, allowing routing decisions (e.g., defer to human) without wasting compute on uncertain queries.

## Key Results

| Metric | SEP | Full SE | Notes |
|--------|-----|---------|-------|
| **Inference cost** | 1 forward pass | 10+ forward passes + NLI | ~10x cheaper |
| **In-distribution AUROC** | Comparable | Baseline | Only -0.5 ± 2.6 AUROC delta vs accuracy probes |
| **OOD AUROC improvement** | +7.7 to +10.5 | — | vs accuracy probes on Llama-2/Mistral/Phi-3 |
| **Training data** | 2,000 examples | — | Minimal supervision |

The key advantage over **accuracy probes** (which predict correctness directly): SEP generalizes better out-of-distribution because it predicts a model-intrinsic property (semantic entropy) rather than an external label (accuracy).

## Practical Considerations

- **Layer selection**: Mid-to-late layers encode semantic uncertainty most strongly
- **OOD robustness**: The main selling point — accuracy probes overfit to training domain, SEP doesn't
- **Models evaluated**: Llama-2-7B/70B, Mistral-7B, Phi-3-3.8B, Llama-3-70B
- **Datasets**: TriviaQA, SQuAD, BioASQ, NQ Open
- **Limitation**: Still requires a labeled training set (to compute SE as supervision); the probe itself is linear, so cannot capture complex uncertainty patterns

## Related Terms

- [Semantic Entropy](term_semantic_entropy.md) — The quantity SEP is trained to predict; SEP amortizes SE computation
- [Bidirectional Entailment](term_bidirectional_entailment.md) — Used during training to compute SE labels; not needed at inference
- [NLI](term_nli.md) — Used during training only; eliminated at inference time
- [Hallucination](term_hallucination.md) — Primary application: cheap hallucination detection via uncertainty
- [LLM](term_llm.md) — Target systems; SEP extracts uncertainty from LLM internals
- [BERT](term_bert.md) — DeBERTa (BERT variant) used for NLI during training phase

## References

- Kossen, Han, Razzak, Schut, Malik, Gal. "Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs." arXiv 2024. [arXiv:2406.15927](https://arxiv.org/abs/2406.15927)
- Farquhar, Kossen, Kuhn, Gal. "Detecting hallucinations in large language models using semantic entropy." Nature 2024. [doi:10.1038/s41586-024-07421-0](https://www.nature.com/articles/s41586-024-07421-0)
- [lit_kuhn2023semantic](../papers/lit_kuhn2023semantic.md) — Foundational Semantic Entropy paper (ICLR 2023)
