---
tags:
  - resource
  - terminology
  - data
  - behavioral_data
  - ml_features
keywords:
  - clickstream
  - browsing behavior
  - page sequences
  - user journey
  - session data
topics:
  - data sources
  - feature engineering
  - behavioral analysis
language: markdown
date of note: 2026-01-30
status: active
building_block: concept
related_docs: https://w.amazon.com/bin/view/Bill2Pay/WebDataAnalyticsTool/research/Clickstream/
---

# Term: Clickstream

## Definition

**Clickstream** is sequential data capturing a customer's browsing behavior on Amazon's website, including page views, navigation paths, timestamps, and interactions. This data is processed from raw query logs and normalized into session-level records that track the complete customer journey from arrival through purchase or contact.

## Full Name

**Clickstream Data** (also: Click Path, Navigation Stream, Session Sequence)

## Purpose

Clickstream data serves multiple purposes in buyer risk prevention:
1. **Behavioral Fingerprinting**: Identify abuse patterns through browsing behavior differences
2. **Intent Prediction**: Predict customer's likely action (return, refund, claim) from navigation
3. **Temporal Analysis**: Compare behavior at different points (ordering vs concession time)
4. **Anomaly Detection**: Detect non-customer traffic (bots, scrapers, associates fraud)

## Architecture

### Data Processing Pipeline

```
Raw Query Logs → HitAssembly → SortedHits → SessionizedHits → Webmon
                     |
                     v
              +----------------+
              | Normalization  |
              | - Timestamps   |
              | - Page Types   |
              | - Ref Markers  |
              +----------------+
                     |
                     v
              +----------------+
              | Sessionization |
              | - Customer ID  |
              | - Session ID   |
              | - Attribution  |
              +----------------+
                     |
                     v
              Clickstream Tables
```

### Data Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Page Type** | Category of page viewed | `gateway`, `DetailPage`, `YourOrders`, `Cart` |
| **Ref Marker** | Tracking tag in URLs | Tracks link performance, attribution |
| **Session** | Grouped clicks by customer | Time-bounded customer journey |
| **Feed** | Country/marketplace | `us`, `uk`, `de`, `jp` |

## Applications in Buyer Abuse Prevention

### 1. RASP Detection (Tattletale)

**Diff Transformer for Clickstream**:
- **Architecture**: [Siamese Network](term_siamese_network.md) comparing clickstream at ordering vs concession time
- **Purpose**: Detect behavioral drift indicative of Refund As Service Provider abuse
- **Performance**: AUC 0.86 → 0.90 with time encoding
- **Reference**: [Tattletale MTR Diff Transformer](../documentation/mtr/mtr_tattletale_2024_03_diff_transformer.md)

### 2. Moderated Enforcement (ME) Customer Behavior

**Behavioral Embeddings**:
- **Architecture**: TF-IDF + LightGBM on page type sequences
- **Purpose**: Predict whether suspended customers will be reinstated
- **Look-back Window**: 2-4 days of clickstream data
- **Features**: Page sequences (e.g., `YourOrders → Spark → YourOrders → gateway-phone-web`)
- **Reference**: [ME Behavioral Model](https://w.amazon.com/bin/view/Users/jhyang/Quip/ModeratedEnforcementCustomerBehaviorModel/)

### 3. Intent Prediction (CS ML)

**Contact Reason Prediction**:
- **Architecture**: LSTM/BiLSTM with page embedding layers
- **Purpose**: Predict most relevant issue/intent from browsing patterns
- **Approach**: Sequential deep learning treating clicks as time-ordered events
- **Reference**: [Clickstream Intent Prediction](https://w.amazon.com/bin/view/CSTech/Machine_Learning/Internal/PersonalizationConcession/Projects/Clickstream/)

### 4. Non-Customer Traffic Detection

**Fraud Detection**:
- **Purpose**: Identify bots, scrapers, and associate fraud
- **Signals**: High volume from single IP, no conversion patterns, embedded pages
- **Reference**: [Clickstream Non-customer Traffic](https://w.amazon.com/bin/view/Weblab/AnalystProjects/ClickstreamNoncustomerTraffic/)

## Technical Details

### Feature Engineering Approaches

| Approach | Description | Use Case |
|----------|-------------|----------|
| **TF-IDF Vectorization** | Convert page sequences to weighted vectors | ME behavior classification |
| **LSTM Embedding** | Learn sequential representations | Intent prediction |
| **Siamese Networks** | Compare two clickstream windows | Behavioral drift detection |
| **Session Statistics** | Aggregate metrics (duration, page count) | Anomaly detection |

### LSTM Model Architecture

```
Input (Page Sequence) → Embedding Layer → LSTM Layer 1 → LSTM Layer 2 → Softmax
                            |
                            v
                 High-dimensional encoding
                 (independence among pages)
```

**Key Design Choices**:
- Embedding layer encodes pages into high dimensions (avoids ordinal assumptions)
- LSTM handles long-term dependencies through memory cells
- Bidirectional LSTM captures both forward and backward patterns

### Data Access

| Source | Description |
|--------|-------------|
| **Clickstream Tables** | Processed session-level data in DW |
| **Clickstream Console** | [console.clickstream.amazon.com](https://console.clickstream.amazon.com/bootcamp) |
| **Onboarding** | [Clickstream User Docs](https://w.amazon.com/index.php/Clickstream/UserDocs/Onboarding) |

## Evolution in Buyer Abuse ML

### Timeline

| Year | Application | Team |
|------|-------------|------|
| 2018 | CS Intent Prediction | CS ML |
| 2020 | ME Behavioral Analysis | BAP ML |
| 2024 | RASP Diff Transformer | Tattletale |

### Current State

Clickstream embeddings are being developed by BAP ML (Ethan/yunxiaow) for:
- ASIN embeddings integration
- Sandstone embedding fusion
- Enhanced behavioral fingerprinting

## Related Terms

- [Traffic Stream](term_traffic_stream.md) - Complementary web event data source (sign-in focused)
- [Siamese Network](term_siamese_network.md) - Architecture for comparing clickstream windows
- [RASP](term_rasp.md) - Refund As Service Provider (detection use case)
- [Tattletale](term_tattletale.md) - MO detection system using clickstream
- [OTF](term_otf.md) - On-The-Fly variables (clickstream features)
- [BSM](term_bsm.md) - Buyer Seller Messaging (complementary behavioral data)
- **[Pub/Sub](term_pub_sub.md)**: Clickstream events are commonly transported via pub/sub topics (Kafka, SNS) for real-time analytics, session replay, and downstream abuse detection pipelines
- **[WebSocket](term_websocket.md)**: WebSocket connections generate real-time clickstream events for interactive sessions, complementing traditional HTTP-based page view tracking

## References

### Amazon Internal
- [Clickstream 101](https://w.amazon.com/bin/view/Bill2Pay/WebDataAnalyticsTool/research/Clickstream/)
- [Clickstream Console Bootcamp](https://console.clickstream.amazon.com/bootcamp)
- [ME Behavioral Embeddings](https://w.amazon.com/bin/view/Users/jhyang/Quip/ModeratedEnforcementCustomerBehaviorModel/)
- [CS ML Intent Prediction](https://w.amazon.com/bin/view/CSTech/Machine_Learning/Internal/PersonalizationConcession/Projects/Clickstream/)
- [Non-customer Traffic Detection](https://w.amazon.com/bin/view/Weblab/AnalystProjects/ClickstreamNoncustomerTraffic/)
- [BAP ML Team Wiki](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/About/Team/)

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Clickstream Data |
| **Purpose** | Capture browsing behavior for abuse detection |
| **Data Type** | Sequential page views, timestamps, session metadata |
| **Key Applications** | RASP detection, intent prediction, ME classification |
| **ML Approaches** | LSTM, BiLSTM, Siamese Networks, TF-IDF |
| **Status** | Active - foundational behavioral data source |
| **Team** | BAP ML (Ethan/yunxiaow for embeddings) |

---

**Last Updated**: January 30, 2026  
**Status**: Active - Key behavioral data source for abuse detection
