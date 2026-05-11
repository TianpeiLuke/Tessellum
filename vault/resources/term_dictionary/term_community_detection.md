---
tags:
  - resource
  - terminology
  - ml_model
  - graph_algorithm
  - tattletale
  - buyer_abuse
keywords:
  - Community Detection
  - graph partitioning
  - Greedy Modularity Maximization
  - modularity
  - EVINCE
  - expansion
  - Tattletale
topics:
  - machine learning
  - graph algorithms
  - abuse detection
language: markdown
date of note: 2026-01-30
status: active
building_block: concept
related_docs: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/
---

# Term: Community Detection

## Definition

**Community Detection** (CD) is a graph partitioning technique used in the Tattletale expansion stage to identify densely connected subgroups ("communities") of accounts within larger clusters. While Tattletale's initial clustering via MODE groups accounts by behavioral similarity, Community Detection further refines these clusters by finding tightly-knit account networks based on relationship density. This allows investigators to prioritize the highest-risk subsets within large clusters, minimizing false positive rates while maximizing abuse detection.

## Full Name

Community Detection (CD)

## Purpose

Community Detection serves multiple purposes in the Tattletale pipeline:
1. **Break down large clusters** - Decompose clusters of 50-200 accounts into manageable 10-30 account communities
2. **Minimize False Positive Rate** - Focus on densely connected accounts most likely to be truly abusive
3. **Improve prioritization accuracy** - Leverage community-level features rather than cluster-level averages
4. **Enhance investigation efficiency** - Provide investigators with tighter, more coherent account groups
5. **Increase MO detection** - Identify abuse patterns that may be diluted in larger clusters

## Context in Buyer Abuse Prevention

### Position in Tattletale Pipeline

Community Detection operates in the **Expansion** stage of the Tattletale pipeline:

```
Seeding → Detection (MODE) → Expansion (EVINCE + CD) → Refinement (SCAP) → TTUX
                                      ↑
                               Community Detection
```

**Problem Solved**: After MODE clusters accounts by behavioral similarity, some clusters are too large and contain both high-risk and low-risk subsets. SCAP prioritization works at cluster level, which can:
- Rank high a cluster that has low-risk subsets
- Queue clusters where only a portion is truly abusive
- Create investigator burden with noisy account groups

**Solution**: Community Detection partitions clusters into smaller, densely connected communities, enabling:
- Community-level risk scoring
- Filtering low-risk communities before queuing
- Higher precision investigation targets

### Algorithm: Greedy Modularity Maximization

**Modularity** measures the quality of graph partitioning by comparing edge density within communities vs. a random graph with the same degree distribution.

**Algorithm Steps**:
1. Start with each account as its own community
2. Iteratively merge neighboring nodes into communities
3. Optimize modularity score at each step
4. Stop when no merge improves modularity

**Mathematical Definition**:
```
Q = (1/2m) × Σ[Aij - (ki×kj)/(2m)] × δ(ci, cj)

Where:
- Aij = adjacency matrix (1 if edge between i and j)
- ki, kj = degree of nodes i and j
- m = total edges in graph
- ci, cj = community assignments
- δ = 1 if same community, 0 otherwise
```

**Intuition**: High modularity = many edges within communities, few edges between communities

### Key Features

**1. Density-Based Grouping**
- Accounts with strong inter-connections grouped together
- Sparse connections between communities indicate different abuse patterns
- Preserves relationship structure from original graph

**2. Community-Level Features**
- Aggregated concession amounts per community
- Order velocity and behavioral patterns
- Risk score distributions within community

**3. Prioritization Enhancement**
- Community-level risk scores complement cluster-level SCAP
- Dense communities with high concessions prioritized
- Low-density or low-risk communities filtered out

## Performance Results

### Launch Impact (July 2023)

| Metric | Before CD | After CD | Improvement |
|--------|-----------|----------|-------------|
| MOs Detected per Month | 71 | 89 | **+25%** |
| False Positive Rate | Higher | Lower | Improved |
| Investigation Precision | Cluster-level | Community-level | Enhanced |

### Key Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| MO Detection Increase | +15% | **+25%** |
| Community Size | 10-30 accounts | Achieved |
| Investigation Time | Reduced | Per-community |

## Implementation Details

### Input
- Clusters from MODE (clusters of 50-200 accounts)
- Account relationship graph (linkages as edges)
- Edge weights (strength of relationships)
- Node features (account attributes)

### Processing
1. **Graph Construction**: Build subgraph for each cluster
2. **Modularity Optimization**: Apply Greedy Modularity Maximization
3. **Community Extraction**: Identify final community partitions
4. **Feature Aggregation**: Compute community-level metrics
5. **Prioritization**: Score communities for investigation

### Output
- Communities (10-30 accounts each)
- Community-level risk scores
- Relationship density metrics
- Queued to TTUX for investigation

### Integration with SCAP

**Before CD**: SCAP ranked entire clusters
**After CD**: SCAP ranks communities within clusters

```
MODE Cluster (100 accounts)
   ↓ Community Detection
Community A (25 accounts, high density) → High SCAP score → Queued
Community B (40 accounts, medium density) → Medium SCAP score → Queued
Community C (35 accounts, low density) → Low SCAP score → Filtered
```

## Deployment Timeline

| Date | Milestone |
|------|-----------|
| Q2 2023 | Experiments started |
| June 30, 2023 | Launched for NCL queue |
| September 1, 2023 | Launched in HeavyHitter queue |
| December 2023 | DNRIN/US expansion |
| March 2024 | All stores worldwide (target) |

## Related Research

### HGT-GRAHIES (2024 Internship Research)

Advanced research exploring **Heterogeneous Graph Transformers** with **hierarchical coarsening** for community-aware MO detection:

- **HGT-GRAHIES**: Achieves F1-score of 0.8421 vs 0.1538 (HGT-base)
- **Entropy Reduction**: 0.36 → 0.11 (improved cluster purity)
- **Precision**: 72.73% with perfect recall
- **MO Clusters**: Identifies 8 vs 4-5 (baseline methods)

**Future Direction**: Heterogeneous-aware coarsening mechanisms for customer-chat graphs.

## Limitations

**1. Computational Cost**
- Modularity optimization is O(n log n) per cluster
- Large clusters require more processing time
- Trade-off with processing frequency

**2. Resolution Limit**
- Small communities may be merged into larger ones
- Very small abuse rings may not be detected as separate communities
- Tuning required for different cluster sizes

**3. Static Graph Assumption**
- Operates on point-in-time relationship snapshot
- Doesn't capture temporal evolution of communities
- Weekly refresh addresses but doesn't eliminate issue

## Best Practices

### For Scientists
- ✅ Test modularity thresholds on labeled MO data
- ✅ Validate community sizes are investigable (10-50 accounts)
- ✅ Monitor community-level vs cluster-level metrics
- ✅ Compare with Consensus Clustering results

### For Investigators
- ✅ Review community boundaries before filtering
- ✅ Check inter-community relationships for missed patterns
- ✅ Report communities that should be merged/split
- ✅ Provide feedback on community quality

## Ownership & Support

**Team**: BAP ML Tattletale
**Contact**: buyer-abuse-ml-tattletale@amazon.com
**Wiki**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/

## Related Terms

**Pipeline Components**:
- [Tattletale](term_tattletale.md) - Parent MO detection system
- [MODE](term_mode.md) - MO Detection Engine (clustering before CD)
- [EVINCE](term_evince.md) - Expansion stage (includes CD)
- [SCAP](term_scap.md) - Cluster/community prioritization
- [TTUX](term_ttux.md) - Visualization platform

**Related Algorithms**:
- [Consensus Clustering](term_consensus_clustering.md) - Alternative clustering approach
- [Modularity](term_modularity.md) - Graph metric optimized by CD
- [Graph Neural Networks](term_gnn.md) - Advanced graph ML
- [GraphRAG](term_graphrag.md) - Graph-based RAG using Leiden community detection for hierarchical summarization (Edge et al., 2024)

**Research References**:
- [GraphRAG (Edge et al., 2024)](../papers/lit_edge2024local.md) — Uses Leiden community detection to partition entity knowledge graphs into hierarchical communities for global sensemaking

**Abuse Detection**:
- [MAA (Multi-Account Abuse)](term_maa.md) - Primary abuse type
- [MO (Modus Operandi)](term_mo.md) - Abuse patterns detected
- [ARM (Abuse Risk Mining)](term_arm.md) - Investigation team

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Community Detection (CD) |
| **Purpose** | Partition large clusters into densely connected communities for better investigation |
| **Algorithm** | Greedy Modularity Maximization |
| **Pipeline Position** | Expansion stage (after MODE, before SCAP) |
| **Key Benefit** | +25% MO detection improvement |
| **Launch Date** | July 2023 (NCL), September 2023 (HeavyHitter) |
| **Output** | Communities of 10-30 accounts with risk scores |
| **Team** | BAP ML Tattletale |
| **Status** | ✅ Active - deployed to multiple queues |

**Key Insight**: Community Detection bridges the gap between large behavioral clusters (MODE) and individual account investigation. By identifying the **dense cores** within clusters, CD ensures investigators focus on the most suspicious account networks while filtering out loosely connected accounts that may be false positives. The 25% improvement in MO detection validates that **relationship density** is a strong signal of coordinated abuse - accounts in tight communities are more likely to be working together on the same MO than accounts with sparse connections.

---

**Last Updated**: January 30, 2026  
**Status**: Active - deployed in Tattletale expansion stage  
**Next Review**: Q2 2026 - expansion to all stores worldwide
