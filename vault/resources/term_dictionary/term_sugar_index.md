---
tags:
  - resource
  - terminology
  - metric
  - abuse_detection
  - financial_risk
keywords:
  - Sugar Index
  - SI
  - concession ratio
  - abuse metric
  - TTM
  - trailing twelve months
topics:
  - abuse detection metrics
  - risk quantification
  - concession analysis
language: python
date of note: 2026-03-14
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/TRMS_Abuse_Methodology/
---

# Term: Sugar Index (SI)

## Definition

**Sugar Index (SI)** is a core metric in Amazon's abuse prevention programs that measures the ratio of concessions (refunds, replacements, credits) received by a customer to their total order value over a trailing twelve month (TTM) period. The metric quantifies how much financial benefit ("sweetness") a customer extracts from Amazon relative to their spending, making it a fundamental indicator for identifying potentially abusive behavior.

## Full Name

SI = **Sugar Index**

Also referred to as: **Concession Ratio**, **Abuse Index**

## Etymology: Why "Sugar"?

The term "Sugar" Index derives from the metaphor of **sweetness** or **benefit** that customers extract from Amazon:

- **"Sweet Deal"**: High SI customers are getting exceptionally "sweet" benefits from Amazon
- **Disproportionate Benefit**: SI measures how much customers are "sweetening" their deals through concessions
- **Risk Indicator**: Like consuming too much sugar is unhealthy, high SI indicates unhealthy customer behavior
- **Financial Extraction**: The index quantifies the "sweetness" (monetary value) extracted beyond normal shopping

The metaphor captures the essence of abuse: customers exploiting Amazon's customer-friendly policies to extract disproportionate value (sweetness) relative to their legitimate purchases.

## Basic Formula

### Standard Sugar Index

```
Sugar Index (SI) = (Total Concession Amount in TTM) / (Total Order Amount in TTM) × 100%
```

**Components**:
- **Numerator**: Sum of all concession dollar amounts granted in trailing 12 months
- **Denominator**: Sum of all order dollar amounts placed in trailing 12 months
- **Result**: Percentage representing concession-to-order ratio

**Example**:
- Customer orders: $1,000 in past 12 months
- Concessions received: $400 in past 12 months
- Sugar Index = $400 / $1,000 = 40% SI

### Interpretation

**Low SI (0-10%)**:
- Normal customer behavior
- Typical return/refund patterns
- Low abuse risk

**Medium SI (10-30%)**:
- Elevated concession rate
- Requires monitoring
- May indicate borderline behavior

**High SI (30-50%)**:
- Very high concession rate
- Strong abuse indicator
- Likely enforcement action

**Extreme SI (50%+)**:
- Extracting more value through concessions than legitimate shopping
- Clear abuse signal
- Immediate investigation required

**Over 100% SI**:
- Receiving more in concessions than spent on orders
- "Hit and Run" abuse pattern
- Urgent enforcement needed

## Key Highlights

**Abuse-Type Thresholds and Regional Calibration**: Each abuse program (DNR, FLR, NSR, MDR, RR, PDA) calculates its own program-specific Sugar Index using the same concession-to-order ratio formula but with program-specific concession amounts in the numerator. Graduated thresholds (e.g., DNR_SI: 50% for 1+ concessions, 25% for 2+, 10% for 3+) balance frequency with intensity, and regional calibrations account for marketplace differences in return behavior, fraud patterns, and local policies across NA, EU, and FE regions.

**Advanced Variations and Statistical Smoothing**: Smoothed SI applies Bayesian shrinkage to stabilize the metric for low-volume customers by pulling individual SI toward the population mean, reducing false positives from new accounts with volatile ratios. Cluster SI aggregates the metric across related accounts to detect coordinated multi-account abuse, and the Smoothed Small Concession Sugar Index (SSCSI) caps concessions per order to remove CS agent error impact.

**Operational Integration and Limitations**: In practice, SI serves as the foundation for abuse definition rules, a top-ranked ML model feature (across XGBoost, Random Forest, and neural networks), an ARI investigation prioritization signal, and a real-time risk scoring variable computed via OTF with sub-100ms latency. Known limitations include new-account bias, legitimate high-SI scenarios (defective products, sizing issues), cluster attribution complexity, and order value normalization challenges -- all of which require combining SI with additional signals and human review.

## See Also

- **[Sugar Index: Abuse-Type Specific Thresholds and Regional Considerations](../policy_sops/sop_sugar_index_abuse_type_thresholds.md)** -- program-specific SI formulas (DNR, FLR, NSR, MDR, RR, PDA), abuse thresholds, currency conversion, regional threshold calibration
- **[Sugar Index: Practice, Automation, and Technical Implementation](../policy_sops/sop_sugar_index_practice_and_automation.md)** -- abuse definition framework, ML model features, investigation workflow, real-time risk scoring, threshold tuning, data pipeline, storage and access
- **[Sugar Index: Advanced Variations](../analysis_thoughts/thought_sugar_index_advanced_variations.md)** -- Smoothed SI, SSCSI, Cluster SI, statistical normalization for low-volume customers and multi-account detection
- **[Sugar Index: Limitations, Time Windows, and Best Practices](../analysis_thoughts/thought_sugar_index_limitations_and_time_windows.md)** -- TTM rationale, alternative time windows, new account bias, legitimate high-SI scenarios, cluster attribution, order value normalization, best practices

## FAQ

- **[FAQ: What CX Metrics Should I Monitor for Silent Failures?](../faqs/faq_cx_metrics_silent_failures.md)** — Sugar Index distribution drift as upstream data health signal
- **[FAQ: Is there a partial refund policy at Amazon?](../faqs/faq_partial_refund_policy.md)** — Sugar Index determines graduated enforcement tier for restocking fees

---

## Related Concepts

### Metrics

- **Concession Count**: Number of concessions (used alongside SI)
- **Order Count**: Number of orders (SI denominator factor)
- **GMS (Gross Merchandise Sales)**: Alternative to order amount
- **Retrocharge Success Rate**: Related to failed return patterns

### Programs Using SI

- **[Area: FLR](../../areas/area_flr.md)** - Failed Returns abuse detection
- **[Area: DNR](../../areas/area_dnr.md)** - Delivered Not Received detection
- **[Area: MDR](../../areas/area_mdr.md)** - Materially Different Returns
- **[Area: NSR](../../areas/area_mdr.md)** - Non-Sellable Returns
- **[Area: MAA](../../areas/area_maa.md)** - Multi-Account Abuse (cluster SI)

### Tools and Systems

- **[Tool: OTF](../tools/tool_otf.md)** - Real-time SI computation and serving
- **[Tool: Paragon](../tools/tool_paragon.md)** - SI displayed in investigation UI
- **[Term: GMRA](term_gmra.md)** - SI used in Gather phase variables
- **[Term: URES](term_ures.md)** - SI variables fed to risk evaluation

- **[Defect Index](term_defect_index.md)**: Category-normalized concession rate (CUBES approach to the same measurement problem)
- **[Differentiated Treatment](term_differentiated_treatment.md)**: Operational use of concession metrics for treatment routing
- **[Holdout Analysis](term_holdout_analysis.md)**: SI feeds into closure decisions whose false positive rate is measured by holdout analysis

## References

### Primary Documentation

- [TRMS Abuse Methodology](https://w.amazon.com/bin/view/TRMS_Abuse_Methodology/) - Official abuse definitions using SI
- [Concession Abuse Prevention](https://w.amazon.com/bin/view/AbusePrevention/ConcessionAbusePrevention/) - Historical SI-based prevention
- [AFN Analytics](https://w.amazon.com/bin/view/BuyerAbuseDataScience/Analytics/ProgramsAnalytics/AFN/) - SI metrics and thresholds

### Model Reports

- [Small Concession Abuse Model](https://w.amazon.com/bin/view/Small_Concession_Abuse_Final_Model_-_12_month_observation_period/) - Smoothed SI methodology
- [EU Small Concession Model](https://w.amazon.com/bin/view/Small_Concession_Abuse_Final_Model_-_EU_-_12_month_observation_period/) - Regional SI calibration
- Various abuse model reports use SI as primary feature

### Analytics Resources

- [Weekly Top 10 Abuse Customers](https://w.amazon.com/bin/view/TRMS_Weekly_Top_10_Abuse_Customers_Investigation/) - SI-based ranking
- [MODE (MO Detection)](https://w.amazon.com/bin/view/BuyerAbuseDataScience/Science/MODE/) - Beyond SI: behavior-based detection

## Summary

**Sugar Index (SI)** is the cornerstone metric for abuse detection at Amazon, quantifying the ratio of concessions to orders as a measure of the "sweetness" or financial benefit customers extract. The name "Sugar" metaphorically represents the disproportionate benefit abusers gain through concessions relative to legitimate shopping.

With variations spanning different abuse types (DNR_SI, FLR_SI, NSR_SI, MDR_SI, etc.), time windows (30/90/180/365 days), and aggregation levels (individual, cluster), Sugar Index provides a flexible, quantifiable framework for:
- **Defining Abuse**: Threshold-based rules (e.g., FLR_SI ≥ 70%)
- **ML Features**: Top predictor in abuse detection models
- **Investigation Prioritization**: High-SI cases reviewed first
- **Real-Time Decisions**: OTF-served SI for instant risk scoring

While powerful, SI should never be used in isolation. Best practice combines SI with concession counts, order volumes, absolute dollar amounts, cluster analysis, and human investigation to balance effective abuse prevention with excellent customer experience.

---

**Last Updated**: March 14, 2026
**Status**: Active - Core metric across all abuse prevention programs
**Next Review**: Continuous monitoring and threshold adjustment
