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

FPR (False Positive Rate) is the proportion of legitimate (non-abusive) cases incorrectly classified as abusive by a model or rule. FPR = FP / (FP + TN), where FP is false positives and TN is true negatives. In abuse prevention, FPR directly measures the rate at which genuine customers are wrongly impacted by enforcement actions — a critical metric because false positives erode customer trust and generate costly appeals.

## Context

- **BAP guardrail**: Models operate at defined FPR thresholds (typically 1% FPR for PFW models)
- **Customer impact**: Each false positive = genuine customer wrongly denied, cancelled, or investigated
- **Tradeoff**: Lower FPR means fewer genuine customers impacted but also lower recall (more abuse missed)
- **Measurement**: Offline evaluation on holdout sets; online via control groups and appeal/reversal rates

## Key Characteristics

- **Complement of specificity**: FPR = 1 - Specificity
- **ROC curve**: FPR is the x-axis of ROC curves; AUC measures overall FPR-TPR tradeoff
- **Operating point**: BAP models select operating points balancing FPR vs recall ($recall)
- **Cost asymmetry**: In abuse prevention, false positives (impacting genuine customers) are typically more costly than false negatives (missing abuse)
- **Related to precision**: At low base rates (rare abuse), even low FPR can yield many false positives

## Related Terms

- **[Precision](term_precision.md)**: Complementary metric — proportion of flagged cases that are truly abusive
- **[Sugar Index](term_sugar_index.md)**: Risk score calibrated against FPR targets
- **[PFOC](term_pfoc.md)**: Pre-fulfilment cancellation — operates at strict FPR to avoid wrongly cancelling orders
- **[DeepCare](term_deepcare.md)**: Auto-pass model — FPR measures wrongly passed abusive cases
- **[Holdout Analysis](term_holdout_analysis.md)**: Measurement methodology that directly quantifies FPR for account closures by holding out 10% of closures and observing behavior over 90 days

## References

- [Wikipedia: False Positive Rate](https://en.wikipedia.org/wiki/False_positive_rate)
