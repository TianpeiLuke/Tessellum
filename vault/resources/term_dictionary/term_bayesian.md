---
tags:
  - resource
  - terminology
  - statistics
  - probability
  - inference
keywords:
  - Bayesian
  - Bayesian inference
  - prior
  - posterior
  - Bayes theorem
  - probabilistic
  - conjugate prior
topics:
  - statistics
  - probability theory
language: markdown
date of note: 2026-04-16
status: active
building_block: concept
related_wiki: null
---

# Bayesian (Bayesian Inference)

## Definition

Bayesian inference is a statistical framework that updates probability estimates as new evidence is observed, using Bayes' theorem: P(θ|data) ∝ P(data|θ) × P(θ). The prior distribution encodes existing beliefs, the likelihood captures observed data, and the posterior distribution represents updated beliefs. In BAP, Bayesian methods are used in A/B testing, model calibration, reinforcement learning exploration, and uncertainty quantification.

## Context

- **BAP applications**: Bayesian A/B testing for model evaluation, Thompson sampling for explore-exploit, uncertainty estimation for model confidence
- **Research**: Referenced in BRP ML research on continual learning, bandits, and probabilistic models

## Key Characteristics

- **Prior + likelihood → posterior**: Systematic belief updating with evidence
- **Uncertainty quantification**: Produces probability distributions, not point estimates
- **Sequential updating**: Naturally handles streaming data and online learning
- **Conjugate priors**: Analytical solutions for common distribution families

## Related Terms

- **[FPR](term_fpr.md)**: False Positive Rate — Bayesian methods for threshold optimization
- **[Precision](term_precision.md)**: Bayesian estimation of model precision
- **[Drift Detection](term_drift_detection.md)**: Bayesian change-point detection
- **[Deep Learning](term_deep_learning.md)**: Bayesian neural networks for uncertainty
