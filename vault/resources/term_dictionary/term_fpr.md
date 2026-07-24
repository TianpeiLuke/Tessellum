---
tags:
  - resource
  - terminology
  - machine_learning
  - evaluation_metrics
  - statistics
keywords:
  - FPR
  - False Positive Rate
  - Type I error
  - specificity
  - model evaluation
  - precision recall tradeoff
topics:
  - model evaluation
  - statistics
language: markdown
date of note: 2026-04-16
status: active
building_block: concept
---

# FPR - False Positive Rate

## Definition

FPR (False Positive Rate) is the proportion of negative (non-target) cases incorrectly classified as positive by a model or rule. FPR = FP / (FP + TN), where FP is false positives and TN is true negatives. In abuse and fraud detection, FPR measures the rate at which legitimate cases are wrongly flagged — a critical metric because false positives erode user trust and generate costly appeals and manual review.

## Context

- **Threshold selection**: Models are often operated at a defined FPR threshold (e.g., 1% FPR) to bound the impact on legitimate cases
- **User impact**: Each false positive represents a genuine user wrongly denied, cancelled, or investigated
- **Tradeoff**: Lower FPR means fewer legitimate cases impacted but also lower recall (more true positives missed)
- **Measurement**: Offline evaluation on holdout sets; online via control groups and appeal/reversal rates

## Key Characteristics

- **Complement of specificity**: FPR = 1 - Specificity
- **ROC curve**: FPR is the x-axis of ROC curves; AUC measures the overall FPR-TPR tradeoff
- **Operating point**: Classifiers select operating points balancing FPR against recall
- **Cost asymmetry**: In abuse prevention, false positives (impacting genuine users) are typically more costly than false negatives (missing abuse)
- **Related to precision**: At low base rates (rare positives), even a low FPR can yield many false positives

## Related Terms

- **[Precision](term_precision.md)**: Complementary metric — proportion of flagged cases that are truly positive
- **[Holdout Analysis](term_holdout_analysis.md)**: Measurement methodology that quantifies FPR by holding out a fraction of enforced cases and observing subsequent behavior

## References

- [Wikipedia: False Positive Rate](https://en.wikipedia.org/wiki/False_positive_rate)
