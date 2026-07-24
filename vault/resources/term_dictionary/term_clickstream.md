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
---

# Term: Clickstream

## Definition

**Clickstream** is sequential data capturing a user's browsing behavior on a website, including page views, navigation paths, timestamps, and interactions. This data is processed from raw query/request logs and normalized into session-level records that track the complete user journey from arrival through conversion or exit.

## Full Name

**Clickstream Data** (also: Click Path, Navigation Stream, Session Sequence)

## Purpose

Clickstream data serves multiple purposes in behavioral analytics and risk detection:
1. **Behavioral Fingerprinting**: Identify patterns through browsing-behavior differences
2. **Intent Prediction**: Predict a user's likely next action from navigation
3. **Temporal Analysis**: Compare behavior at different points in a journey
4. **Anomaly Detection**: Detect non-human traffic (bots, scrapers) and unusual activity

## Architecture

### Data Processing Pipeline

```
Raw Query Logs → Hit Assembly → Sorted Hits → Sessionized Hits → Analytics Store
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
              | - User ID      |
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
| **Page Type** | Category of page viewed | `gateway`, `DetailPage`, `Orders`, `Cart` |
| **Ref Marker** | Tracking tag in URLs | Tracks link performance, attribution |
| **Session** | Grouped clicks by user | Time-bounded user journey |
| **Feed** | Country/marketplace | `us`, `uk`, `de`, `jp` |

## Applications in Behavioral Analysis

### 1. Behavioral Drift Detection

**Diff / Comparison Models**:
- **Architecture**: [Siamese Network](term_siamese_network.md) comparing clickstream from two different windows
- **Purpose**: Detect behavioral drift between points in a user journey
- **Signal**: Time encoding of events improves discrimination of behavioral change

### 2. Reinstatement / Churn Prediction

**Behavioral Embeddings**:
- **Architecture**: TF-IDF + gradient-boosted trees on page-type sequences
- **Purpose**: Predict future user behavior from recent browsing
- **Look-back Window**: A few days of clickstream data
- **Features**: Page sequences (e.g., `Orders → Search → Orders → gateway`)

### 3. Intent Prediction

**Contact/Action Reason Prediction**:
- **Architecture**: LSTM/BiLSTM with page-embedding layers
- **Purpose**: Predict the most relevant intent from browsing patterns
- **Approach**: Sequential deep learning treating clicks as time-ordered events

### 4. Non-Human Traffic Detection

**Bot/Scraper Detection**:
- **Purpose**: Identify bots, scrapers, and automated traffic
- **Signals**: High volume from single IP, no conversion patterns, atypical page access

## Technical Details

### Feature Engineering Approaches

| Approach | Description | Use Case |
|----------|-------------|----------|
| **TF-IDF Vectorization** | Convert page sequences to weighted vectors | Behavior classification |
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

## Related Terms

- [Siamese Network](term_siamese_network.md) - Architecture for comparing clickstream windows
- **[Pub/Sub](term_pub_sub.md)**: Clickstream events are commonly transported via pub/sub topics (Kafka, SNS) for real-time analytics, session replay, and downstream detection pipelines
- **[WebSocket](term_websocket.md)**: WebSocket connections generate real-time clickstream events for interactive sessions, complementing traditional HTTP-based page view tracking

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Clickstream Data |
| **Purpose** | Capture browsing behavior for analytics and detection |
| **Data Type** | Sequential page views, timestamps, session metadata |
| **Key Applications** | Behavioral drift, intent prediction, bot detection |
| **ML Approaches** | LSTM, BiLSTM, Siamese Networks, TF-IDF |
| **Status** | Active - foundational behavioral data source |

---

**Last Updated**: January 30, 2026  
**Status**: Active - key behavioral data source for analytics and detection
