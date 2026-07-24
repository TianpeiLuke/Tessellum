---
tags:
  - resource
  - terminology
  - ml
  - metric
  - model_evaluation
keywords:
  - Precision
  - Positive Predictive Value
  - PPV
  - false positive
  - classification metric
  - TP
  - FP
topics:
  - machine learning
  - model evaluation
  - classification metrics
language: markdown
date of note: 2026-02-03
status: active
building_block: concept
---

# Precision - Positive Predictive Value

## Definition

**Precision** (also known as **Positive Predictive Value** or **PPV**) is a classification metric that measures the proportion of positive predictions that are actually correct. It answers the question: "Of all the cases my model flagged as positive, how many are actually positive?"

**Formula**:
```
Precision = TP / (TP + FP)

Where:
- TP = True Positives (correctly identified positives)
- FP = False Positives (negatives incorrectly flagged as positive)
```

**Key Insight**: High precision means when the model says "this is positive," it's usually right. Low precision means many false alarms.

## Why Precision Matters

In many applications, **false positives (FP)** carry significant costs:

1. **User Experience Damage**: Blocking or flagging legitimate users harms trust
2. **Operational Burden**: Reviewers waste time investigating false alarms
3. **Reputation Risk**: Wrongly acting on a legitimate case damages credibility
4. **Downstream Cost**: A false positive can trigger a costly, sometimes irreversible action

**Illustrative Context**: A model with 60% precision means 40% of flagged cases are actually negative - potentially causing 4 out of 10 flagged users to have a bad experience.

## Precision vs Recall Trade-off

| Metric | Optimizes For |
|--------|---------------|
| **Precision** | Minimize False Positives |
| **Recall** | Minimize False Negatives |

**The Trade-off**:
- Raising the classification threshold → Higher precision, lower recall
- Lowering the threshold → Higher recall, lower precision
- You cannot maximize both simultaneously

> "Precision is a good measure to use when the cost of a False Positive is high."

When false positives (acting on legitimate cases) are more costly than false negatives (missing some true positives), precision is often prioritized.

## Precision in Different Contexts

### By Decision Stakes

| Decision Type | Precision Target | Rationale |
|---------------|------------------|-----------|
| **Irreversible automated action** | ≥98% | Permanent, high impact, no human check |
| **Reversible automated action** | ≥95% | Disruptive but recoverable |
| **Queue to human review** | ≥80% | Human review catches FPs |
| **Advisory signal / banner** | ≥70% | Informational only, no action taken |

### By Detection Stage

**Real-time / inline prevention**:
- Higher precision required (≥95%)
- Acting on a request immediately impacts the user
- FPs are immediately visible

**Batch / offline queuing**:
- Lower precision acceptable (≥80%)
- Manual investigation validates before action
- Time to review before acting

**Retrospective analysis**:
- Lowest precision acceptable (≥60%)
- Discovery / research context
- No direct user impact

## Precision Calculation Examples

### Basic Example

```python
# Scenario: Model evaluates 1000 cases
# Model flags 100 as positive
# Manual review finds: 85 actual positives, 15 negatives

TP = 85   # True positives (correctly identified)
FP = 15   # False positives (negatives flagged as positive)

Precision = TP / (TP + FP) = 85 / 100 = 0.85 = 85%
```

### Multi-threshold Analysis

```python
from sklearn.metrics import precision_score, precision_recall_curve

# y_true: actual labels (0 or 1)
# y_scores: model prediction scores

# Precision at default threshold (0.5)
y_pred = (y_scores >= 0.5).astype(int)
precision = precision_score(y_true, y_pred)

# Precision-Recall curve at all thresholds
precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)

# Find threshold for target precision (e.g., 90%)
target_precision = 0.90
idx = np.argmin(np.abs(precisions - target_precision))
optimal_threshold = thresholds[idx]
```

### Precision@K (Top-K Precision)

For ranked outputs (e.g., a prioritized queue), evaluate precision at the top K results:

```python
def precision_at_k(y_true, y_scores, k):
    """Precision in top K scored items"""
    # Sort by score descending
    sorted_indices = np.argsort(y_scores)[::-1][:k]
    # Count true positives in top K
    tp_at_k = y_true[sorted_indices].sum()
    return tp_at_k / k

# Example: Precision in top 100 highest-scored items
precision_100 = precision_at_k(y_true, y_scores, k=100)
```

## Threshold Validation Process

A typical process for setting a threshold to meet a precision target:

```
1. Train model on historical labeled data
2. Generate predictions on a holdout set
3. Sample positive predictions for manual audit
4. Calculate precision from audit results
5. Adjust threshold until target precision is achieved
6. Deploy with the validated threshold
```

### Continuous Precision Monitoring

**Continuous Validation**:
- Route a small control fraction to manual review
- Calculate precision as the agreement rate with reviewers
- Alert if precision drops below the target

**Key Metric**:
```
Model Precision = # cases where model agrees with reviewer / # reviewed cases
```

### Precision-Recall AUC (PR AUC)

For imbalanced data, PR AUC is often more informative than ROC AUC:

**Average Precision (AP)**:
```
AP = Σ (Rₙ - Rₙ₋₁) × Pₙ

Where Pₙ and Rₙ are precision and recall at the nth threshold
```

**PR AUC Interpretation**:
- Higher is better (maximum = 1.0)
- Random classifier: PR AUC ≈ positive class rate
- Sensitive to class imbalance

## Confusion Matrix Context

| | Predicted Positive | Predicted Negative |
|--|-------------------|-------------------|
| **Actual Positive** | TP (True Positive) | FN (False Negative) |
| **Actual Negative** | FP (False Positive) | TN (True Negative) |

**Precision** = TP / (TP + FP) → Column-wise on predicted positives

**Related Metrics**:

| Metric | Formula | Focus |
|--------|---------|-------|
| **Precision** | TP / (TP + FP) | Quality of positive predictions |
| **Recall** | TP / (TP + FN) | Coverage of actual positives |
| **Specificity** | TN / (TN + FP) | Quality of negative predictions |
| **NPV** | TN / (TN + FN) | Negative Predictive Value |
| **F1 Score** | 2 × (P × R) / (P + R) | Harmonic mean of P and R |
| **F-beta** | (1+β²) × (P × R) / (β² × P + R) | Weighted P-R balance |

## When to Prioritize Precision

### High Precision Required

1. **Irreversible decisions**: Permanent actions must be confident
2. **Blocking legitimate activity**: Stops valid use if wrong
3. **User-facing accusations**: Wrongly accusing users is costly
4. **Automation without human review**: No safety net for FPs

### Lower Precision Acceptable

1. **Queue prioritization**: Humans validate before acting
2. **Advisory signals**: Informational only
3. **Research / discovery**: Finding new patterns
4. **Internal reporting**: No direct user impact

## Improving Precision

### Model-Level Improvements

1. **Raise Classification Threshold**: Trade recall for precision
2. **Better Features**: More discriminative variables
3. **Cleaner Training Data**: Reduce label noise
4. **Class Rebalancing**: Undersample positives, oversample negatives
5. **Ensemble Methods**: Combine multiple models

### Operational Improvements

1. **Multi-Stage Filtering**: High precision → queue → human review
2. **Confidence Scores**: Only act on high-confidence predictions
3. **Segmentation**: Different thresholds for different populations
4. **Human-in-the-Loop**: Route uncertain cases to reviewers

## External Resources

- **sklearn precision_score**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html
- **sklearn precision_recall_curve**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html

## Related Terms

### ML Metrics
- **[Recall](term_recall.md)** - True Positive Rate / Sensitivity
- **[AUC](term_auc.md)** - Area Under the ROC Curve
- **[F1 Score](term_f1_score.md)** - Harmonic mean of Precision and Recall
- **[FPR](term_fpr.md)** - False Positive Rate
- **[FP](term_fp.md)** - False Positive (a negative case flagged as positive)

### Threshold Setting
- **[Control Group](term_control_group.md)** - Precision validation mechanism
- **[Operational Point](term_operational_point.md)** - FPR/TPR trade-off point
- **[Score Calibration](term_score_calibration.md)** - Mapping scores to probabilities

## Summary

**Precision Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Precision (Positive Predictive Value / PPV) |
| **Formula** | TP / (TP + FP) |
| **Range** | 0.0 to 1.0 (higher is better) |
| **Measures** | Quality of positive predictions |
| **Minimizes** | False Positives (FP) |
| **Trade-off** | Higher precision → lower recall |
| **When Critical** | Irreversible actions, blocking, automation |
| **Tools** | sklearn.metrics.precision_score |

**Key Insight**: When false positives directly harm legitimate users, precision is often the primary guardrail. A model with 90% precision and 60% recall is frequently preferred over 60% precision and 90% recall, because the cost of acting on legitimate cases typically exceeds the cost of missing some true positives.

**Operational Guidance**:
- **Set the precision target first** based on decision stakes
- **Adjust the threshold** to achieve the target precision
- **Monitor precision** via control groups and audits
- **Accept the recall trade-off** as the cost of user trust

---

**Last Updated**: February 3, 2026
**Status**: Active - Fundamental ML evaluation metric
**Domain**: Machine Learning, Model Evaluation
