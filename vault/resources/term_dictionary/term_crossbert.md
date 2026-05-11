---
tags:
  - resource
  - terminology
  - ml_model
  - foundation_model
  - deep_learning
  - identity_entities
keywords:
  - CrossBERT
  - cross-attention BERT
  - foundation model
  - identity representation
  - X2R
  - email2risk
  - domain2risk
  - textual identity
topics:
  - foundation models
  - identity entity modeling
  - buyer abuse prevention
language: markdown
date of note: 2026-01-30
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ERA/
related_launch: 2026-01-27_launch-announcement-crossbert-a-foundational-model-for-learning-unified.md
---

# CrossBERT - Foundational Model for Textual Identity Entities

## Definition

**CrossBERT** (Cross-attention Bidirectional Encoder Representations from Transformers) is a foundational model developed by the Buyer Abuse Prevention (BAP) ML team in collaboration with Payment Risk (PR) for learning unified representations from textual identity entities.

**Key Characteristic**: CrossBERT consolidates multiple specialized point-solution models (email2risk, domain2risk) into a single, unified architecture using cross-attention mechanisms to capture inter-correlations between different entity types.

## Why CrossBERT Matters

**The Problem**: Historically, textual identity entities (emails, names, domains) were processed by a fragmented landscape of point-solution models:
- Each model used different architectures
- Separate development, training, and maintenance pipelines
- Couldn't capture inter-correlations between entity types

**CrossBERT Solution**: A unified model architecture that:
- Can be fine-tuned for different downstream use cases
- Captures patterns that simpler models miss
- Reduces operational complexity and technical debt
- Enables faster deployment of new capabilities

## Model Architecture

### Dual-Stream Transformer with Cross-Attention

```
┌─────────────────┐    ┌─────────────────┐
│   Stream 1      │    │   Stream 2      │
│  (Entity Type A)│    │  (Entity Type B)│
├─────────────────┤    ├─────────────────┤
│  Self-Attention │◄──►│  Self-Attention │
├─────────────────┤    ├─────────────────┤
│ Cross-Attention │◄──►│ Cross-Attention │
├─────────────────┤    ├─────────────────┤
│     Fusion      │◄──►│     Fusion      │
└─────────────────┘    └─────────────────┘
```

**Processing Stages**:
1. **Separate Streams**: Different textual identity entities processed independently
2. **Self-Attention Layers**: Capture internal patterns within each entity type
3. **Cross-Attention Fusion**: Information flows between streams
4. **Progressive Refinement**: Multiple rounds for refined representations

## Primary Application: X2R (X2Risk)

The first production deployment of CrossBERT:

**Fine-Tuning Approach**:
- Input: Customer identity data (email handles, account names, email domains)
- Stream 1: Email handle + account name pairs
- Stream 2: Email domain + placeholder (for symmetry)
- Output: Fused embeddings for binary abuse risk classification

**Deployment**:
- Powers two abuse prevention rules in US PFW intent
- Identifies potentially abusive orders for manual review
- **Impact**: ~$2M/year savings

## Performance Benchmarks

| Metric | CrossBERT Advantage |
|--------|---------------------|
| **vs. Competitors** | 50-150 bps improvement |
| **Fine-tuning Speed** | 30-50% faster than general-purpose LLMs |
| **Time to Production** | Faster iteration cycles |

## Evolution & History

| Date | Milestone |
|------|-----------|
| **2023** | Initial concept proposed by Principal Scientist Olcay Boz |
| **2023** | First version implemented by Zheng Lu (Payment Risk) |
| **2026** | Production launch with architectural validation |

**Key Advances in Current Version**:
1. Systematic architecture exploration (multi-level interaction vs. late fusion)
2. Scaled pre-training to 100M entity pairs
3. Complementary pre-training objectives (generative + discriminative)

## Roadmap

| Timeline | Milestone |
|----------|-----------|
| **Q1 2026** | Deprecate email2risk/domain2risk, unify on CrossBERT |
| **Q1 2026** | Expand to additional PFW rulesets |
| **Q2 2026** | Pilot email/name similarity in IDA and COSA |
| **Q4 2026** | Consolidate all x2risk models across BRP |
| **Q4 2026** | Pre-train region-specific models (EU, FE) |

## Team Ownership

| Team | Contributors |
|------|-------------|
| **BAP ML** | Bo Jiang, Yina Gu |
| **PR ML** | Jia Geng, Wuji Liu, Yibing Wu, Zheng Lu, Zora Zhang |
| **Leadership** | Olcay Boz, Hakan Brunzell, Kyle Muramatsu, Saurab Nog |

## Related Terms

- [BERT](term_bert.md) - Base Transformer architecture
- [BAP](term_bap.md) - Buyer Abuse Prevention team
- [PFW](term_pfw.md) - Pre-Fulfillment Workflow
- [IDA](term_ida.md) - Identity Association model (future consumer)
- [COSA](term_cosa.md) - Continuous One Step Ahead (future consumer)
- [Email2Risk](term_email2risk.md) - Legacy model being replaced
- [Domain2Risk](term_domain2risk.md) - Legacy model being replaced

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Cross-attention Bidirectional Encoder Representations from Transformers |
| **Purpose** | Unified representations from textual identity entities |
| **Architecture** | Dual-stream Transformer with cross-attention |
| **Entity Types** | Email handles, names, domains |
| **First Application** | X2R (X2Risk) for abuse detection |
| **Deployment** | US PFW intent rules |
| **Team** | BAP ML + Payment Risk ML |
| **Launch** | January 2026 |

**Key Insight**: CrossBERT represents a shift from point-solution models to foundational architecture. Rather than maintaining separate email2risk, domain2risk, name2risk models, teams can fine-tune a single pretrained foundation for any identity-based risk scoring task.

## References

### Primary Documentation
- [Email Risk Assessment (ERA) Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ERA/)
- [Email2Risk Consortium Model](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ERA/Email2Risk_Consortium_Model/)
- [Domain2Risk Model](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ERA/ModelTraining/)

### Related Programs
- [TRMS Abuse Analytics Model Reports](https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/)
- [Buyer Abuse Launch Announcements](https://w.amazon.com/bin/view/BuyerAbuse/Status/LaunchAnnouncements/)

### Launch Announcement
- [CrossBERT Launch (January 2026)](../../archives/launch_announcements/2026-01-27_launch-announcement-crossbert-a-foundational-model-for-learning-unified.md)

---

**Last Updated**: January 30, 2026  
**Status**: Active - newly launched foundation model  
**Contact**: Bo Jiang (bjjin@), Olcay Boz (olcayboz@)
