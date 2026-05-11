---
tags:
  - resource
  - terminology
  - ml
  - metric
  - model_evaluation
keywords:
  - F1 Score
  - F1-Score
  - harmonic mean
  - precision
  - recall
  - F-measure
  - F-beta
topics:
  - machine learning
  - model evaluation
  - classification metrics
  - abuse detection
language: markdown
date of note: 2026-02-03
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Internal/Models/Model_Review/
---

# F1 Score - Harmonic Mean of Precision and Recall

## Definition

**F1 Score** (also known as **F-measure** or **F1**) is a classification metric that combines precision and recall into a single number using the **harmonic mean**. It provides a balanced measure of model performance when both false positives and false negatives matter.

**Formula**:
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)

Where:
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
```

**Key Insight**: F1 Score balances the trade-off between precision and recall. A high F1 means the model is effective at both correctly identifying positive instances AND minimizing false positives and false negatives.

## Why Harmonic Mean?

The F1 Score uses the **harmonic mean** rather than the arithmetic mean for an important reason:

> "A simple average can sometimes be biased towards higher values. In situations where we need a more conservative evaluation, we use the Harmonic Mean. The Harmonic Mean is always less than or equal to the simple average, giving more weight to the smaller values."

**Example**:
```
Precision = 90%, Recall = 30%

Arithmetic Mean = (90 + 30) / 2 = 60%
Harmonic Mean (F1) = 2 × (0.9 × 0.3) / (0.9 + 0.3) = 45%
```

The harmonic mean gives a more **conservative, realistic** evaluation when precision and recall differ significantly. A model with 90% precision but only 30% recall isn't truly "60% good" - the F1 score of 45% better reflects its imbalanced performance.

## F1 Score Interpretation

| F1 Score | Interpretation |
|----------|----------------|
| **1.0** | Perfect precision AND recall (ideal) |
| **0.8 - 1.0** | Excellent balance |
| **0.6 - 0.8** | Good balance |
| **0.4 - 0.6** | Moderate performance |
| **< 0.4** | Poor balance (P and R significantly different) |
| **0.0** | Either precision or recall is zero |

**Key Property**: F1 = 0 if either precision OR recall is 0, regardless of the other value. Both must be non-zero for F1 > 0.

## F1 Score in Buyer Abuse Prevention

### When to Use F1 Score

F1 Score is most useful in BAP when:

1. **Both FP and FN are costly**: Need to balance catching abuse (recall) with protecting good customers (precision)
2. **No clear priority**: Can't decide whether precision or recall matters more
3. **Model comparison**: Comparing models with different precision-recall trade-offs
4. **Threshold selection**: Finding the optimal threshold that balances both metrics

### BAP F1 Score Standards

**Typical Ranges**:
- **Excellent**: F1 ≥ 0.85
- **Good**: F1 0.70 - 0.85
- **Acceptable**: F1 0.60 - 0.70
- **Needs Improvement**: F1 < 0.60

**Example Model Performance** (from internal documentation):
- CSMO HGT-GRAHIES MO Detection: F1 = 0.84
- Spam classification example: F1 = 0.71 (Precision 67%, Recall 75%)

### F1 vs Precision/Recall Priority

| Scenario | Primary Metric | Why |
|----------|---------------|-----|
| **Auto-enforcement** | Precision | FP cost (wrongly accusing customers) is high |
| **MO Detection** | Recall | FN cost (missing abuse patterns) is high |
| **Investigation Queue** | F1 Score | Balance between queue quality and coverage |
| **Research/Discovery** | Recall | Maximize pattern discovery |

**BAP Guidance**: 
> "F1 Score is a useful metric when both Precision and Recall are critical factors."

In most BAP workflows, **precision is prioritized** over F1 because customer experience impact (FP) is typically more costly than missed abuse (FN). However, F1 is valuable for:
- Model development comparisons
- Threshold optimization
- Balanced queue sizing

## F1 Score Calculation Examples

### Basic Example

```python
# Scenario: Model evaluates 100 cases
# TP = 30 (correctly identified abuse)
# FP = 15 (legitimate cases flagged as abuse)
# FN = 10 (abuse cases missed)

Precision = 30 / (30 + 15) = 0.67 = 67%
Recall = 30 / (30 + 10) = 0.75 = 75%

F1 = 2 × (0.67 × 0.75) / (0.67 + 0.75) = 0.71 = 71%
```

### Python Implementation

```python
from sklearn.metrics import f1_score, precision_recall_fscore_support

# y_true: actual labels (0 or 1)
# y_pred: predicted labels (0 or 1)

# F1 Score at default threshold
f1 = f1_score(y_true, y_pred)

# Get all metrics together
precision, recall, f1, support = precision_recall_fscore_support(
    y_true, y_pred, average='binary'
)

# For multi-class: macro (unweighted) vs micro (weighted)
f1_macro = f1_score(y_true, y_pred, average='macro')  # Treat classes equally
f1_micro = f1_score(y_true, y_pred, average='micro')  # Weight by class size
```

### F1 Threshold Optimization

```python
from sklearn.metrics import precision_recall_curve

# y_true: actual labels
# y_scores: model prediction scores

precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)

# Calculate F1 at each threshold
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)

# Find threshold that maximizes F1
best_idx = np.argmax(f1_scores)
best_threshold = thresholds[best_idx]
best_f1 = f1_scores[best_idx]
```

## F-beta Score: Weighted F1

When precision and recall have **unequal importance**, use the F-beta score:

**Formula**:
```
F_β = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```

**Beta Interpretation**:
- **β = 1**: F1 Score (equal weight to P and R)
- **β > 1**: Recall is more important (e.g., β = 2 weights recall 2× more)
- **β < 1**: Precision is more important (e.g., β = 0.5 weights precision 2× more)

**BAP Use Cases**:

| Beta | Use Case | Rationale |
|------|----------|-----------|
| **β = 0.5** | Auto-enforcement | Precision twice as important |
| **β = 1** | Investigation queue | Balance both metrics |
| **β = 2** | MO discovery | Recall twice as important |

```python
from sklearn.metrics import fbeta_score

# F0.5 (precision-weighted)
f05 = fbeta_score(y_true, y_pred, beta=0.5)

# F2 (recall-weighted)
f2 = fbeta_score(y_true, y_pred, beta=2)
```

## Multi-Class F1 Averaging

For multi-class classification (e.g., abuse type classification):

### Macro F1 (Unweighted Average)

```
Macro F1 = (F1_class1 + F1_class2 + ... + F1_classN) / N
```

- Treats all classes equally
- Better for imbalanced datasets where minority classes matter
- Used when each abuse type is equally important

### Micro F1 (Weighted Average)

```
Micro F1 = 2 × (Total TP) / (2 × Total TP + Total FP + Total FN)
```

- Weights by class frequency
- Equals accuracy for multi-class single-label classification
- Used when overall correctness matters more than per-class performance

### Weighted F1

```
Weighted F1 = Σ(support_class × F1_class) / Total support
```

- Weights by class support (number of true instances)
- Balances between macro and micro

## Confusion Matrix Context

| | Predicted Positive | Predicted Negative |
|--|-------------------|-------------------|
| **Actual Positive** | TP (True Positive) | FN (False Negative) |
| **Actual Negative** | FP (False Positive) | TN (True Negative) |

**F1 Score** = 2 × (P × R) / (P + R) → Combines row and column metrics

**Related Metrics**:

| Metric | Formula | Relationship to F1 |
|--------|---------|-------------------|
| **Precision** | TP / (TP + FP) | Component of F1 |
| **Recall** | TP / (TP + FN) | Component of F1 |
| **Accuracy** | (TP + TN) / Total | Different metric (includes TN) |
| **F-beta** | Weighted F1 | Generalization of F1 |

## When F1 Score Is Misleading

### Class Imbalance

F1 can be misleading for highly imbalanced data:

```
Example: 99% negative, 1% positive (abuse is rare)

Model predicts all positive → Recall = 100%, Precision = 1%
F1 = 2 × (0.01 × 1.0) / (0.01 + 1.0) = 0.02

This seems low, but the model caught ALL abuse (100% recall)
```

**Solution**: Use **PR AUC** or **precision at specific recall** for imbalanced abuse detection.

### Different Error Costs

F1 treats FP and FN equally, but in BAP:
- FP (blocking good customer) might cost $10 in CX damage + $100 in lost revenue
- FN (missing abuse) might cost $50 in concession loss

**Solution**: Use **cost-sensitive metrics** or **F-beta** with appropriate beta.

### Threshold Dependency

F1 requires binary predictions (not scores), so depends on chosen threshold:

```
Same model, different thresholds:
- Threshold 0.3: F1 = 0.65
- Threshold 0.5: F1 = 0.71
- Threshold 0.7: F1 = 0.60

Which F1 represents the model? 
```

**Solution**: Report F1 at specific operational thresholds, or use **AUC** for threshold-independent comparison.

## Documentation Links

### Primary Documentation

**BAP Model Review**:
- **Model Reports**: https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/ - F1 metrics
- **CSMO HGT**: https://w.amazon.com/bin/view/SPS_Graph_Modeling_Working_Group/ - F1 0.84 for MO detection

**Technical References**:
- **ML Metrics Wiki**: https://w.amazon.com/bin/view/Users/Andriy/learning/ml-metrics/ - F1 calculation examples
- **KYT-AI**: https://w.amazon.com/bin/view/TOPS_Tech_Team/COMS/KYT-AI/ - F1 and harmonic mean explanation

### External Resources

- **sklearn f1_score**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
- **sklearn fbeta_score**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fbeta_score.html

## Related Terms

### ML Metrics
- **[Precision](term_precision.md)** - Positive Predictive Value (component of F1)
- **[Recall](term_recall.md)** - True Positive Rate (component of F1)
- **[AUC](term_auc.md)** - Area Under the ROC Curve
- **[Binomial Distribution](term_binomial_distribution.md)** — Precision and recall are proportions; confidence intervals use binomial/beta models
- **[Beta Distribution](term_beta_distribution.md)** — Bayesian estimation of F1 components uses Beta posteriors

### BAP Concepts
- **[PR AUC](term_pr_auc.md)** - Precision-Recall Area Under Curve
- **[Operational Point](term_operational_point.md)** - Threshold selection
- **[QPD](term_qpd.md)** - Queue Per Day (capacity planning)

### Model Evaluation
- **[Confusion Matrix](term_confusion_matrix.md)** - TP/FP/TN/FN breakdown
- **[Accuracy](term_accuracy.md)** - Overall correctness (different from F1)

## Summary

**F1 Score Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | F1 Score (F-measure, F1) |
| **Formula** | 2 × (Precision × Recall) / (Precision + Recall) |
| **Range** | 0.0 to 1.0 (higher is better) |
| **Type** | Harmonic mean of Precision and Recall |
| **Measures** | Balance between catching abuse and avoiding false alarms |
| **Best For** | When both FP and FN costs matter equally |
| **BAP Usage** | Model comparison, threshold optimization, balanced queuing |
| **Limitation** | Requires threshold; treats FP=FN cost equally |
| **Generalization** | F-beta (β>1 favors recall, β<1 favors precision) |
| **Tools** | sklearn.metrics.f1_score, fbeta_score |

**Key Insight for BAP**: F1 Score is valuable for model development and comparison when you need a single number to summarize precision-recall balance. However, in production BAP workflows, **precision or recall individually** is typically more actionable because they map directly to business outcomes:
- **Precision** → Customer experience / false alarm rate
- **Recall** → Abuse coverage / detection rate

Use F1 for:
- Comparing models during development
- Optimizing classification thresholds
- Reporting balanced performance to stakeholders

Use Precision/Recall directly for:
- Setting operational thresholds
- Production monitoring
- Business impact analysis

---

**Last Updated**: February 3, 2026
**Status**: Active - Fundamental ML evaluation metric
**Domain**: Machine Learning, Model Evaluation, Buyer Abuse Prevention
