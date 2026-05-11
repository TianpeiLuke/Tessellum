---
tags:
  - resource
  - terminology
  - uncertainty_quantification
  - information_theory
  - llm
  - nlp
keywords:
  - semantic entropy
  - uncertainty estimation
  - meaning space
  - hallucination detection
  - linguistic invariance
  - entropy
  - natural language generation
topics:
  - Uncertainty Quantification
  - Large Language Models
  - Information Theory
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# Semantic Entropy (SE)

## Definition

**Semantic Entropy** is an uncertainty measure for large language models that computes entropy over **meaning equivalence classes** rather than token sequences. Given an input question, the LLM generates multiple candidate answers via sampling. These answers are clustered into groups of semantically equivalent responses using bidirectional NLI entailment, and entropy is computed over the resulting meaning clusters weighted by their aggregate token-level probabilities.

**Full Name**: Semantic Entropy

**Key formula**:

$$SE(x) = -\sum_{c \in C} p(c|x) \log p(c|x)$$

where C is the set of meaning clusters and p(c|x) = Σ_{s∈c} p(s|x) sums token-level probabilities across all surface forms in cluster c.

**Key property**: SE ≤ PE (predictive entropy) always holds. The gap represents "wasted" entropy from lexical variation among semantically equivalent outputs.

## Why It Matters

Standard predictive entropy (token-level) systematically **overestimates** uncertainty when a model generates diverse but equivalent phrasings. For example, "Paris", "The capital of France is Paris", and "It's Paris" all convey the same meaning but spread probability mass across different token sequences. Semantic entropy correctly assigns low uncertainty in this case.

This makes SE a principled **hallucination detector**: high SE indicates the model is generating semantically diverse (genuinely uncertain) answers, while low SE indicates consistent meaning regardless of surface form.

## How It Works

1. **Generate**: Sample M candidate answers from the LLM at temperature T (typically T=0.5, M=10)
2. **Cluster**: Use a [bidirectional entailment](term_bidirectional_entailment.md) classifier ([NLI](term_nli.md) model, typically DeBERTa-large) to group semantically equivalent answers
3. **Aggregate**: Sum token-level probabilities within each meaning cluster
4. **Compute**: Calculate entropy over the cluster probability distribution

## Key Properties

| Property | Description |
|----------|-------------|
| SE ≤ PE | Always less than or equal to predictive entropy |
| SE = 0 | When all generations share the same meaning (confident model) |
| SE = PE | When every generation has a unique meaning (no clustering effect) |
| Unsupervised | Requires no labeled data for uncertainty estimation |
| Model-agnostic | Works with any LLM that supports sampling and log-probabilities |

## Practical Considerations

- **Compute cost**: M forward passes + O(M²) NLI calls per query (10 generations → ~45 NLI pairs worst case)
- **Optimal hyperparameters**: T=0.5 (temperature), M=10 (generations) per Kuhn et al. ablation
- **NLI dependency**: Quality bounded by the NLI classifier's accuracy on the target domain
- **Best for**: Free-form generation tasks (QA, summarization); not needed for classification tasks

## Related Terms

- [Bidirectional Entailment](term_bidirectional_entailment.md) — The semantic equivalence test used to form meaning clusters
- [NLI](term_nli.md) — Natural Language Inference; the classifier family used as the entailment oracle
- [Perplexity](term_perplexity.md) — Related metric; predictive entropy ≈ log(perplexity). SE improves on perplexity-based uncertainty
- [Conformal Prediction](term_conformal_prediction.md) — SE extends to conformal prediction sets over meanings for calibrated uncertainty
- **[Multinomial Distribution](term_multinomial_distribution.md)** — Token-level predictions follow multinomial; entropy measures uncertainty over this distribution
- **[Dirichlet Distribution](term_dirichlet_distribution.md)** — Dirichlet prior over token probabilities connects to entropy estimation
- [Hallucination](term_hallucination.md) — SE is a principled detector of LLM hallucinations
- [LLM](term_llm.md) — Target systems for semantic entropy
- [Semantic Entropy Probes](term_semantic_entropy_probes.md) — Linear probes that predict SE from hidden states in a single forward pass
- [Uncertainty-Aware Generation](term_uncertainty_aware_generation.md) — Closed-loop paradigm that uses SE as a control signal to improve generation

- **[Concentration Inequality](term_concentration_inequality.md)**: Entropy estimation error bounds use concentration inequalities

## References

- Kuhn, Gal, Farquhar. "Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation." ICLR 2023 (Spotlight). [arXiv:2302.09664](https://arxiv.org/abs/2302.09664)
- Farquhar, Kuhn, et al. "Detecting hallucinations in large language models using semantic entropy." Nature 2024. [doi:10.1038/s41586-024-07421-0](https://www.nature.com/articles/s41586-024-07421-0)
- [lit_kuhn2023semantic](../papers/lit_kuhn2023semantic.md) — Literature note for the foundational ICLR 2023 paper
