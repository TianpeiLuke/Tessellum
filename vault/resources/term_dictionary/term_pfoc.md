---
tags:
  - resource
  - terminology
  - workflow
  - abuse_prevention
  - order_cancellation
keywords:
  - PFOC
  - Pre-Fulfillment Order Cancellation
  - automated cancellation
  - ID verification
  - safelist
  - PFW
topics:
  - abuse prevention
  - order processing
  - automated enforcement
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/PFOC/
related_quip: https://quip-amazon.com/zMZuAoez7OI8/PFW-Order-Cancellation-PFOC
---

# PFOC - Pre-Fulfillment Order Cancellation

## Definition

**PFOC** stands for **Pre-Fulfillment Order Cancellation**. It is an automated abuse prevention mechanism that evaluates and cancels high-risk orders during the Pre-Fulfillment Workflow (PFW) without requiring manual investigation by ARI (Abuse Risk Investigation). Unlike the traditional PFW Account Closure (PFAC) process, PFOC cancels orders without closing customer accounts.

**Key Function**: Automatically cancel medium-to-high risk orders before fulfillment to prevent abuse while minimizing customer friction.

**Launch**: May 23, 2022 (US), expanded to EU markets June 2022

## Background and Problem Statement

### Previous State: PFW Account Closure (PFAC)

**Traditional Process**:
1. ML model detects high-risk order in PFW
2. Order queued to ARI for manual investigation
3. ARI reviews account for closure
4. If account closed, all pending orders cancelled

**Limitations**:
- **ARI Capacity Constraints**: Manual review limited scalability
- **High Bar for Enforcement**: SOP required very strong evidence for account closure
- **Missed Opportunities**: Medium-risk orders couldn't be actioned due to high closure bar
- **Poor Customer Experience**: Account closure, order cancellation, difficult appeal process

### PFOC Solution

**Key Innovations**:
- **Lower Bar**: Cancel orders without closing accounts
- **Automation**: No manual ARI review required (for auto-cancel rules)
- **Scalability**: Process thousands more orders daily
- **Better CX**: Customers can verify ID and place new orders
- **Evidence Collection**: ID Verification (IDV) via Persona as appeal mechanism

## Key Highlights

**Workflow and Operations**: PFOC operates as a five-step automated pipeline -- order evaluation via URES/GMRA using ML models (LANTERN, COSA) and RMP rules, automatic cancellation with full refund, IDV appeal via Persona, safelist mechanism (90-180 days via OTF), and optional manual writeback review by ARI. Special considerations include mandatory B2B order exclusion, 3% holdout groups for impact measurement, country-specific legal/compliance requirements, and a clear boundary between concessions abuse (PFOC scope) and payment fraud (Payment Risk team scope). See [SOP: PFOC Workflow](../../areas/pfoc_workflow.md) for full details.

**Architecture and Comparison**: PFOC complements PFAC in a two-tier enforcement model -- PFOC handles medium-risk orders via fully automated cancellation while PFAC reserves manual ARI review for the highest-risk account closures. The technical stack integrates upstream systems (PFW, URES, OTF, OWEN), downstream services (APWS, GPO, CSSW, Persona, Nautilus), and lateral components (IDV Service, CHS, FeatureHub). IDV is powered by Persona via the IVV team, with ID data stored in a red-certified warehouse for multi-program use across PFOC, CAP, and ARI. See [Thought: PFOC Architecture and Comparison](../../areas/pfoc_architecture_and_comparison.md) for full details.

**Business Impact and Metrics**: PFOC projected $30M+ in annual global savings at launch, with rule-level breakdowns showing ARI_Model_Rule at $24M, US_DNR_Abusive_Relation at $6M, and US_AFN_High_Risk_Orders at $5M. Operationally, it reduced ARI manual investigation load by ~70% and scaled order evaluation from ~200/week (PFAC) to thousands/week with <100ms latency. Live across US, CA, UK, DE, FR, IT, ES with regional ML models, covering DNR, PDA, MDR/NSR, and MAA abuse vectors. Key quality metrics include >90% enforcement precision target and <1% writeback rate. See [Thought: PFOC Business Impact](../../areas/pfoc_business_impact.md) for full details.

## Related Programs and Systems

### Related Buyer Abuse Programs

- **PDA Prevention**: PFOC mechanism for Pre-Delivery Abuse
- **MAA (Multi-Account Abuse)**: LANTERN, COSA, PACMAN models
- **CAP Routing**: PFOC prevents orders, CAP handles contacts
- **RI (Refund Interception)**: Post-fulfillment complement

### Related Workflows

- **PFW** (Pre-Fulfillment Workflow): Parent workflow containing PFOC
- **PFAC** (PFW Account Closure): Higher-risk complement requiring ARI
- **PCW** (Post-Concession Workflow): Handles abuse after concessions granted

## Documentation and Resources

**Primary Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/PFOC/

**Design Document**: https://quip-amazon.com/zMZuAoez7OI8/PFW-Order-Cancellation-PFOC

**Related Wikis**:
- **PDA Prevention**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/Pre_Delivery_Abuse/
- **IDV**: https://w.amazon.com/bin/view/BuyerAbuse/Engineering/IDV/
- **MAA/MALTA**: https://w.amazon.com/bin/view/MLAnalyticsOnboarding/MALTA/
- **PFW**: https://w.amazon.com/bin/view/ECSG/Ordering/COW/Services/Workflows/Prefulfillment/

**Dashboards**:
- **PFOC Performance**: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/c58ccbd7-dfd4-4919-aec6-f72dec207ba0
- **IDV Metrics**: Included in PFOC dashboard
- **LANTERN**: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/ec7f331a-c8cb-4e90-84a0-346d9e7e000d

**Support**:
- **Buyer Abuse Team**: brp-buyer-abuse@
- **Office Hours**: Weekly intake for questions/onboarding

## FAQ

- **[FAQ: How Do NUTS, OBE, PFOC, IDA, and MAA Models Overlap and Connect?](../faqs/faq_nuts_obe_pfoc_ida_maa_overlap.md)** — How PFOC consumes MAA signals via LANTERN for automated order cancellation

---

## Related Terms

- [PFW](term_pfw.md) - Pre-Fulfillment Workflow (parent workflow)
- [PDA](term_pda.md) - Pre-Delivery Abuse (primary use case)
- [DNR](term_dnr.md) - Delivered Not Received (abuse vector)
- [MAA](term_maa.md) - Multi-Account Abuse (detection models)
- [ARI](term_ari.md) - Abuse Risk Investigation (manual review team)
- [URES](term_ures.md) - Unified Risk Evaluation System (evaluation platform)
- [OTF](term_otf.md) - On The Fly (safelist variable storage)
- [CAP](term_cap.md) - Concessions Abuse Prevention (complementary program)
- [Holdout Analysis](term_holdout_analysis.md) - PFOC holdout groups measure false positive cancellation rate (referenced in PFOC operational considerations)

## See Also

- [SOP: PFOC Workflow and Operational Considerations](../../areas/pfoc_workflow.md) -- Full end-to-end PFOC process (order evaluation, cancellation, IDV appeal, safelist, writeback review) and operational considerations (B2B exclusion, holdout groups, legal compliance, fraud vs abuse boundary)
- [Thought: PFOC Architecture, Integration, and Comparison with PFAC](../../areas/pfoc_architecture_and_comparison.md) -- PFOC vs PFAC comparison table, RMP rules configuration, upstream/downstream/lateral integration points, and IDV/Persona integration details including ID data storage
- [Thought: PFOC Business Impact, Coverage, and Metrics](../../areas/pfoc_business_impact.md) -- Financial savings projections, operational efficiency gains, customer experience metrics, geographic rollout timeline, abuse vector coverage, and monitoring dashboards

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Pre-Fulfillment Order Cancellation |
| **Purpose** | Automated cancellation of medium-to-high risk orders pre-fulfillment |
| **Launch** | May 2022 (US), June 2022 (EU) |
| **Trigger** | PFW evaluation matching PFOC cancel rules |
| **Decision** | Automated (no manual ARI review) |
| **Action** | Cancel order + refund + send IDV request |
| **Appeal** | ID Verification via Persona |
| **Safelist** | 90-180 days after successful IDV |
| **Bar** | Lower than account closure, higher than pass |
| **Savings** | $30M+ annually (projected) |
| **Platform** | URES + RMP + IDV + Persona |
| **Coverage** | DNR, PDA, MDR/NSR, MAA |

**Key Insight**: PFOC represents a **paradigm shift** in buyer abuse prevention - moving from high-bar manual account closures to scalable automated order cancellations. By lowering the enforcement bar and introducing ID verification as an appeal mechanism, PFOC enables Amazon to prevent significantly more abuse while maintaining acceptable customer experience. The combination of ML models (LANTERN, COSA), rule-based evaluation (RMP), and evidence collection (IDV) creates a powerful, self-service system that saves millions annually while reducing operational burden on ARI teams.

---

**Last Updated**: March 15, 2026
**Status**: Active - core abuse prevention mechanism in production WW
