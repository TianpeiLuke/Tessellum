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
  - abuse detection
language: markdown
date of note: 2026-02-03
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Internal/Models/Model_Review/
---

# Precision - Positive Predictive Value

## Definition

**Precision** (also known as **Positive Predictive Value** or **PPV**) is a classification metric that measures the proportion of positive predictions that are actually correct. It answers the question: "Of all the cases my model flagged as abuse, how many are actually abusive?"

**Formula**:
```
Precision = TP / (TP + FP)

Where:
- TP = True Positives (correctly identified abuse)
- FP = False Positives (legitimate cases incorrectly flagged as abuse)
```

**Key Insight**: High precision means when the model says "this is abuse," it's usually right. Low precision means many false alarms.

## Importance in Buyer Abuse Prevention

### Why Precision Matters

In buyer abuse prevention, **false positives (FP)** have significant costs:

1. **Customer Experience Damage**: Blocking/flagging legitimate customers harms trust
2. **Concession Cost**: Incorrectly denying concessions to legitimate claims
3. **Operational Burden**: Investigators waste time reviewing false alarms
4. **Brand Reputation**: Wrongly accusing customers damages Amazon's reputation
5. **Revenue Loss**: Blocking good customers reduces sales

**Business Context**: A model with 60% precision means 40% of flagged cases are legitimate customers - potentially causing 4 out of 10 customers to have bad experiences.

### BAP Precision Standards

**Production Thresholds**:
- **Minimum for production**: Precision ≥ 90%
- **High-confidence automation**: Precision ≥ 95%
- **Conservative enforcement**: Precision ≥ 98%

**Example Model Precision** (from internal documentation):
- MENA Promotion Abuse Model: 91.1% - 99% precision (varies by marketplace)
- CMK Content Moderation: 89-90% precision at 92% recall
- DeepCARE Automation: 90%+ precision (5% control group validation)
- GreenTEA CAP Automation: ~99% precision for auto-enforcement

### Precision vs Recall Trade-off

| Metric | Optimizes For | BAP Context |
|--------|---------------|-------------|
| **Precision** | Minimize False Positives | Protect legitimate customers |
| **Recall** | Minimize False Negatives | Catch all abuse |

**The Trade-off**:
- Raising the classification threshold → Higher precision, lower recall
- Lowering the threshold → Higher recall, lower precision
- You cannot maximize both simultaneously

**BAP Philosophy**: 
> "Precision is a good measure to determine when the costs of False Positive is high."

In abuse prevention, false positives (blocking good customers) are generally more costly than false negatives (missing some abuse), so precision is often prioritized.

## Precision in Different Contexts

### By Enforcement Action Severity

| Action Type | Precision Target | Rationale |
|-------------|------------------|-----------|
| **Account Closure** | ≥98% | Permanent, high customer impact |
| **Order Cancellation** | ≥95% | Reversible but disruptive |
| **Queue to Investigation** | ≥80% | Human review catches FPs |
| **Risk Signal/Banner** | ≥70% | Advisory only, no block |

### By Detection Stage

**Real-time Prevention (PFW)**:
- Higher precision required (≥95%)
- Blocking orders impacts customer experience
- FPs immediately visible to customers

**Batch/Offline Queuing**:
- Lower precision acceptable (≥80%)
- Manual investigation validates
- Time to review before action

**Retrospective Analysis**:
- Lowest precision acceptable (≥60%)
- Discovery/research context
- No direct customer impact

## Precision Calculation Examples

### Basic Example

```python
# Scenario: Model evaluates 1000 orders
# Model flags 100 as abuse
# Manual review finds: 85 actual abuse, 15 legitimate

TP = 85   # True positives (correctly identified abuse)
FP = 15   # False positives (legitimate orders flagged)

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

For ranked outputs (e.g., queuing), evaluate precision at top K results:

```python
def precision_at_k(y_true, y_scores, k):
    """Precision in top K scored items"""
    # Sort by score descending
    sorted_indices = np.argsort(y_scores)[::-1][:k]
    # Count true positives in top K
    tp_at_k = y_true[sorted_indices].sum()
    return tp_at_k / k

# Example: Precision in top 100 riskiest orders
precision_100 = precision_at_k(y_true, y_scores, k=100)
```

## Precision in BAP Workflows

### Model Validation Process

From MENA Promotion Abuse ML documentation:

```
1. Train model on historical abuse data
2. Generate predictions on holdout set
3. Sample positive predictions for manual audit
4. Calculate precision from audit results:
   
   Marketplace  | Precision | Threshold
   -------------|-----------|----------
   UAE          | 94.50%    | 0.98
   Saudi Arabia | 99.00%    | 0.96
   Egypt        | 91.10%    | 0.94
   
5. Adjust threshold until target precision achieved
6. Deploy with validated threshold
```

### DeepCARE Precision Monitoring

**Continuous Validation**:
- 5% control group sent to manual investigation
- Calculate precision as agreement rate with investigators
- Target: ≥90% precision maintained

**Key Metrics**:
```
Model Precision = # cases where model agrees with investigator / # control group cases
```

### Precision-Recall AUC (PR AUC)

For imbalanced abuse data, PR AUC is more informative than ROC AUC:

**Average Precision (AP)**:
```
AP = Σ (Rₙ - Rₙ₋₁) × Pₙ

Where Pₙ and Rₙ are precision and recall at nth threshold
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

1. **Account Closure Decisions**: Permanent action, must be confident
2. **Payment Blocking**: Stops legitimate purchases if wrong
3. **Customer-Facing Messaging**: Accusing customers of abuse
4. **Automation Without Human Review**: No safety net for FPs
5. **High-Value Customer Segments**: CPS/enterprise customers

### Lower Precision Acceptable

1. **Investigation Queue Prioritization**: Humans validate
2. **Risk Signals for Human Decision**: Advisory only
3. **Research/Discovery Analysis**: Finding new patterns
4. **Internal Reporting**: No direct customer impact

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
4. **Human-in-the-Loop**: Route uncertain cases to investigators

### BAP-Specific Strategies

1. **Sugar Index Integration**: Combine with account-level risk
2. **Multi-Vector Validation**: Confirm across abuse types
3. **Temporal Validation**: Check pattern consistency over time
4. **Graph-Based Confirmation**: Validate via network relationships

## Documentation Links

### Primary Documentation

**BAP Model Review**:
- **Model Reports**: https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/ - Performance metrics
- **MENA Promotion ML**: https://w.amazon.com/bin/view/MENA/Keen/Abuse/Projects/PromotionLimitAbuse/ML/ - Precision validation example

**Technical References**:
- **ARI Automation**: https://w.amazon.com/bin/view/IML-NCL/Buyer-Abuse-ARI-Automation/ - Precision@Recall analysis
- **DeepCARE**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/DeepCARE/ - 5% control group validation

### External Resources

- **sklearn precision_score**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html
- **sklearn precision_recall_curve**: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html

## Related Terms

### ML Metrics
- **[Recall](term_recall.md)** - True Positive Rate / Sensitivity
- **[AUC](term_auc.md)** - Area Under the ROC Curve
- **[F1 Score](term_f1_score.md)** - Harmonic mean of Precision and Recall
- **[FPR](term_fpr.md)** - False Positive Rate

### BAP Concepts
- **[FP](term_fp.md)** - False Positive (legitimate case flagged as abuse)
- **[QPD](term_qpd.md)** - Queue Per Day (capacity planning)
- **[DeepCARE](term_deepcare.md)** - Automation with precision monitoring
- **[Control Group](term_control_group.md)** - Precision validation mechanism
- **[Holdout Analysis](term_holdout_analysis.md)** - Measures the complement of precision (false positive rate) for account closures via 90-day holdout observation

### Threshold Setting
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
| **BAP Target** | ≥90% for automation, ≥95% for enforcement |
| **Trade-off** | Higher precision → lower recall |
| **When Critical** | Account closure, payment blocking, automation |
| **Tools** | sklearn.metrics.precision_score |

**Key Insight for BAP**: In buyer abuse prevention, precision is often the primary guardrail because false positives directly harm legitimate customers. A model with 90% precision and 60% recall (catching 60% of abuse with 10% false alarm rate) is often preferred over 60% precision and 90% recall (catching 90% of abuse but 40% false alarm rate) because the cost of wrongly accusing good customers typically exceeds the cost of missing some abuse.

**Operational Guidance**:
- **Set precision target first** based on action severity
- **Adjust threshold** to achieve target precision
- **Monitor precision** via control groups and audits
- **Accept recall trade-off** as cost of customer trust

---

**Last Updated**: February 3, 2026
**Status**: Active - Fundamental ML evaluation metric
**Domain**: Machine Learning, Model Evaluation, Buyer Abuse Prevention
