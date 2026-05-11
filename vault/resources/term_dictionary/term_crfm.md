---
tags:
  - resource
  - terminology
  - ml_model
  - foundation_model
  - deep_learning
  - personalization
keywords:
  - CRFM
  - Customer Representation Foundation Model
  - customer embeddings
  - shopping history
  - personalization
  - decoder transformer
  - M5
  - SFAI
topics:
  - foundation models
  - customer representation
  - personalization
language: markdown
date of note: 2026-01-30
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/Search/Search-M5/Products/
related_quip: https://quip-amazon.com/ymV5AttHCNa5/SFAI-M5-CRFM-Model-Card
related_launch: 2025-11-08_launch-announcement-introducing-crfm-amazon-customer-representation-foundation.md
---

# CRFM - Customer Representation Foundation Model

## Definition

**CRFM** (Customer Representation Foundation Model) is a lightweight decoder-only transformer model developed by the Stores Foundational AI (SFAI) M5 team. It converts an Amazon customer's shopping history into a dense vector representation, capturing clicks, purchases, product details, and timing of interactions.

**Key Characteristic**: CRFM provides a **compact embedding representation** (64 dimensions) of customer behavior, enabling scalable personalization for production systems with strict cost and latency constraints - impossible with hundreds of raw behavior tokens.

## Why CRFM Matters

**The Problem**: Production systems need to understand customer intent for personalization, but:
- Raw behavior data can be hundreds of tokens (clicks, purchases over 1.5 years)
- Large Language Models (LLMs) struggle with long behavior contexts
- Adding raw behavior tokens increases latency significantly
- Confuses Small Language Models (SLMs) lacking reasoning capacity

**CRFM Solution**: Summarizes customer shopping history in a single numeric vector:
- Reduces inference latency and service cost
- Improves scalability for production SLMs
- Embeddings can be refreshed frequently
- Model can be fine-tuned for specific use cases

## Model Architecture

### Technical Specifications

| Component | Details |
|-----------|---------|
| **Architecture** | Decoder-only Transformer |
| **Layers** | 2 |
| **Trainable Parameters** | 87K (lightweight design) |
| **Output Dimensions** | 64-dimensional embedding |
| **Positional Encoding** | Rotary Positional Encoding (temporal awareness) |

### Design Choices
- **Pre-computed Product Embeddings**: Uses cached product vectors instead of processing text on-the-fly
- **Contrastive Loss**: Trained to predict customer's next interaction by aligning customer embedding with subsequent product choice
- **Training Data**: 1.5 years of customer shopping data (clicks, purchases)

## Production Deployments

### Personalized Reranking (P13N)
Two launches in August 2025:

| Feature | Impact |
|---------|--------|
| Homepage Implementation | Launched August 5, 2025 |
| Mobile Cart Widget | Launched August 28, 2025 |
| **Combined OPS Growth** | $238.36MM annualized |

**How it works**: Dynamically reranks product recommendations based on 14-day clicks and 1.5-year purchase history.

### Ads Response Prediction (SP-ARP)
Integration with Early Stage Ranking (ESR) model:

| Metric | Baseline | With CRFM | Improvement |
|--------|----------|-----------|-------------|
| Sourcing Recall@300 | 0.4955 | 0.7296 | +23.41% |
| Ranking MRR | 0.5596 | 0.573 | +1.34% |
| ESR Recall@800 | 0.8372 | 0.9568 | +11.96% |
| Inference Latency | - | 4ms | (efficient) |

## Impact Summary

| Metric | Value |
|--------|-------|
| **Total OPS Growth** | $300MM+ (three P13N launches) |
| **P13N Annualized** | $238.36MM |
| **Recall Improvement** | +23.41% (Ads ARP) |
| **Latency** | 4ms inference |

## Access & Integration

### Getting Started
1. Submit Partner Intake Form with AWS account details and use case
2. Oncall provides access to model artifacts, sample data, code
3. Reference Model Card "How To Use" section

### Resources
- **Slack Channel**: #m5-interest
- **Model Card**: Available via SFAI
- **API Documentation**: M5Lib API documentation (CRFM section)

## Team Ownership

| Team | Contributors |
|------|-------------|
| **SFAI M5** | Zhongruo Wang, Alejandro Mottini, Tian Wang, Chen Xue, Vianne Gao, Skylar Versage, Esther Zhou, Anjali Chadha, Ashwin Kapse, Weiqi Zhang, Qingjun Cui, Ran Xue, Yufan Guo |
| **Leadership** | Xian Li, Bing Yin, Trishul Chilimbi |
| **P13N** | Joe Guo, Lina Liu, Shannie Cheng, Aparna Raman, Steve Ivie |
| **SP-ARP** | Xincheng Lei, Jianwei Liu, Hsien-Ching Kao, Shenghua Bao |

## Potential Applications for Buyer Abuse

While CRFM is primarily designed for personalization, its customer representation capabilities could potentially benefit:
- Customer behavior pattern analysis
- Anomaly detection in shopping behavior
- Abuse risk scoring using behavioral embeddings
- Customer intent classification

## Related Terms

- [LLM](term_llm.md) - Large Language Models
- [BERT](term_bert.md) - Transformer architecture reference
- [Transformer](term_transformer.md) - Foundation architecture
- [DeepCare](term_deepcare.md) - Deep learning investigation automation
- [LILA](term_lila.md) - SFAI's behavior understanding LLM

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Customer Representation Foundation Model |
| **Purpose** | Convert shopping history into dense customer embeddings |
| **Architecture** | Decoder-only Transformer (2 layers, 87K params) |
| **Output** | 64-dimensional customer vector |
| **Training Data** | 1.5 years of customer clicks/purchases |
| **Loss Function** | Contrastive loss |
| **Team** | Stores Foundational AI (SFAI) M5 |
| **Launch** | November 2025 |
| **Impact** | $300MM+ OPS growth |

**Key Insight**: CRFM demonstrates that lightweight, specialized models can outperform general-purpose LLMs for specific production tasks. A 87K parameter model with domain-specific design achieves results that massive models struggle with - particularly when production constraints (latency, cost) matter.

## References

### Primary Documentation
- [M5 Products Wiki](https://w.amazon.com/bin/view/Search/Search-M5/Products/)
- [CRFM Model Card](https://quip-amazon.com/ymV5AttHCNa5/SFAI-M5-CRFM-Model-Card)
- [M5 Day Wiki](https://w.amazon.com/bin/view/Search/Search-M5/M5Day/)

### Related Resources
- **Interest List**: m5-interest@amazon.com
- **Slack Channel**: #m5-interest

### Launch Announcement
- [CRFM Launch (November 2025)](../../archives/launch_announcements/2025-11-08_launch-announcement-introducing-crfm-amazon-customer-representation-foundation.md)

---

**Last Updated**: January 30, 2026  
**Status**: Active - Production deployment across P13N and Ads  
**Contact**: Ran Xue (ranxue@)
