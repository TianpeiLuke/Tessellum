---
tags:
  - resource
  - terminology
  - nlp
  - natural_language_inference
  - semantic_similarity
keywords:
  - bidirectional entailment
  - semantic equivalence
  - NLI
  - DeBERTa
  - textual entailment
  - meaning clustering
topics:
  - Natural Language Processing
  - Semantic Analysis
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Bidirectional Entailment

## Definition

**Bidirectional entailment** is a semantic equivalence test where two texts are considered to have the **same meaning** if and only if each one entails the other. Formally, for texts A and B:

A ≡ B iff (A → B) ∧ (B → A)

where → denotes textual entailment (the premise logically implies the hypothesis).

This is stricter than unidirectional entailment: "Paris is the capital of France" entails "Paris is in France" (one direction), but the reverse does not hold, so they are NOT bidirectionally entailed — they have different meanings.

## Why It Matters

Bidirectional entailment provides a practical, implementable test for **semantic equivalence** in natural language. It is the core mechanism in [Semantic Entropy](term_semantic_entropy.md) for clustering LLM generations into meaning groups. Without it, uncertainty estimation would conflate lexical diversity with genuine semantic uncertainty.

## How It Works

1. Given two text sequences s₁ and s₂ (and optional context x):
   - Run [NLI](term_nli.md) classifier: NLI(x ⊕ s₁, s₂) → {entailment, contradiction, neutral}
   - Run NLI classifier: NLI(x ⊕ s₂, s₁) → {entailment, contradiction, neutral}
2. s₁ ≡ s₂ iff both predictions are "entailment"

In practice, a pre-trained DeBERTa-large model fine-tuned on MNLI is used as the NLI classifier. The question/context x is prepended to the premise to provide disambiguation.

## Clustering Algorithm

Bidirectional entailment is used in a greedy clustering algorithm:

```
For each new generation sᵢ:
  For each existing cluster cₖ:
    If sᵢ ≡ representative(cₖ):
      Add sᵢ to cₖ; stop
  If no match: create new cluster {sᵢ}
```

**Limitation**: This greedy approach is order-dependent — different orderings of inputs can yield different clusterings. The true equivalence relation would require O(M²) pairwise comparisons for perfect partitioning.

## Properties

| Property | Value |
|----------|-------|
| Reflexive | Yes (A entails itself) |
| Symmetric | Yes by construction (both directions required) |
| Transitive | Approximately (NLI classifiers may violate transitivity) |
| Computational cost | 2 NLI calls per pair |

## Related Terms

- [Semantic Entropy](term_semantic_entropy.md) — Uses bidirectional entailment to form meaning clusters for uncertainty estimation
- [NLI](term_nli.md) — The Natural Language Inference task that implements entailment classification
- [BERT](term_bert.md) — DeBERTa (the typical NLI model) is a BERT variant with disentangled attention
- [Hallucination](term_hallucination.md) — Bidirectional entailment enables hallucination detection via semantic entropy

## References

- Kuhn, Gal, Farquhar. "Semantic Uncertainty." ICLR 2023. [arXiv:2302.09664](https://arxiv.org/abs/2302.09664)
- [lit_kuhn2023semantic](../papers/lit_kuhn2023semantic.md) — Paper introducing bidirectional entailment clustering for semantic entropy
