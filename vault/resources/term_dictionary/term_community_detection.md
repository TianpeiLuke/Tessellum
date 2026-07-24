---
tags:
  - resource
  - terminology
  - ml_model
  - graph_algorithm
keywords:
  - Community Detection
  - graph partitioning
  - Greedy Modularity Maximization
  - modularity
  - Leiden
  - Louvain
topics:
  - machine learning
  - graph algorithms
language: markdown
date of note: 2026-01-30
status: active
building_block: concept
---

# Term: Community Detection

## Definition

**Community Detection** (CD) is a graph partitioning technique used to identify densely connected subgroups ("communities") of nodes within a larger graph. Given a graph whose nodes represent entities and whose edges represent relationships, community detection finds groups of nodes with many internal edges and comparatively few edges to the rest of the graph. It is widely used to decompose large clusters into tightly-knit sub-communities, enabling analysis at the level of coherent groups rather than of the graph as a whole.

## Full Name

Community Detection (CD)

## Purpose

Community Detection serves several purposes in graph analysis:
1. **Break down large clusters** - Decompose large, heterogeneous clusters into smaller, coherent communities
2. **Improve prioritization accuracy** - Leverage community-level features rather than whole-graph averages
3. **Enhance interpretability** - Provide tighter, more coherent node groups for downstream analysis
4. **Surface latent structure** - Identify subgroups that may be diluted in a larger graph

## Algorithm: Greedy Modularity Maximization

**Modularity** measures the quality of a graph partition by comparing edge density within communities against a random graph with the same degree distribution.

**Algorithm Steps**:
1. Start with each node as its own community
2. Iteratively merge neighboring nodes into communities
3. Optimize the modularity score at each step
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

**Intuition**: High modularity = many edges within communities, few edges between communities.

### Common Algorithms

| Algorithm | Approach | Notes |
|-----------|----------|-------|
| **Greedy Modularity Maximization** | Iteratively merge to maximize Q | Simple, deterministic |
| **Louvain** | Multi-level modularity optimization | Fast, widely used |
| **Leiden** | Refinement of Louvain | Guarantees well-connected communities |
| **Label Propagation** | Nodes adopt majority neighbor label | Near-linear time |

## Key Features

**1. Density-Based Grouping**
- Nodes with strong inter-connections are grouped together
- Sparse connections between communities indicate distinct structure
- Preserves relationship structure from the original graph

**2. Community-Level Features**
- Aggregated attributes per community
- Structural metrics (density, size, degree distribution)

**3. Prioritization Enhancement**
- Community-level scores complement whole-graph scoring
- Dense communities can be surfaced; low-density ones filtered

## Implementation Details

### Input
- A graph (nodes with attributes, edges with optional weights)
- Optional subgraphs (e.g., per pre-computed cluster)
- Edge weights (strength of relationships)

### Processing
1. **Graph Construction**: Build the (sub)graph
2. **Modularity Optimization**: Apply Greedy Modularity Maximization (or Louvain/Leiden)
3. **Community Extraction**: Identify final community partitions
4. **Feature Aggregation**: Compute community-level metrics
5. **Scoring / Prioritization**: Rank communities for downstream use

### Output
- Communities (node partitions)
- Community-level scores
- Relationship density metrics

## Limitations

**1. Computational Cost**
- Modularity optimization is roughly O(n log n) per graph
- Large graphs require more processing time
- Trade-off with processing frequency

**2. Resolution Limit**
- Small communities may be merged into larger ones
- Very small groups may not be detected as separate communities
- Tuning required for different graph sizes

**3. Static Graph Assumption**
- Operates on a point-in-time relationship snapshot
- Doesn't capture temporal evolution of communities
- Periodic refresh mitigates but doesn't eliminate the issue

## Best Practices

- ✅ Test modularity thresholds/resolution parameters on labeled data
- ✅ Validate community sizes are interpretable for the task
- ✅ Monitor community-level vs whole-graph metrics
- ✅ Compare with alternative approaches (e.g., consensus clustering)
- ✅ Review community boundaries for missed or over-split structure

## Related Terms

**Related Algorithms**:
- [Modularity](term_modularity.md) - Graph metric optimized by community detection
- [Consensus Clustering](term_consensus_clustering.md) - Alternative clustering approach
- [Graph Neural Networks](term_gnn.md) - Advanced graph ML
- [GraphRAG](term_graphrag.md) - Graph-based RAG using Leiden community detection for hierarchical summarization (Edge et al., 2024)

**Research References**:
- [GraphRAG (Edge et al., 2024)](../papers/lit_edge2024local.md) — Uses Leiden community detection to partition entity knowledge graphs into hierarchical communities for global sensemaking

## References

### External Resources
- **"From Local to Global: A GraphRAG Approach to Query-Focused Summarization"** (Edge et al., 2024): https://arxiv.org/abs/2404.16130
- **Louvain method** (Blondel et al., 2008): https://arxiv.org/abs/0803.0476
- **Leiden algorithm** (Traag et al., 2019): https://www.nature.com/articles/s41598-019-41695-z
- **NetworkX community detection**: https://networkx.org/documentation/stable/reference/algorithms/community.html

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Community Detection (CD) |
| **Purpose** | Partition graphs into densely connected communities |
| **Algorithm** | Greedy Modularity Maximization (also Louvain, Leiden) |
| **Key Metric** | Modularity (Q) |
| **Output** | Node communities with density metrics and scores |
| **Status** | Active - core graph analysis technique |

**Key Insight**: Community Detection bridges the gap between large graphs and individual-node analysis. By identifying the **dense cores** within a graph, it lets analysis focus on the most cohesive node groups while filtering out loosely connected nodes. **Relationship density** is a strong structural signal — nodes in tight communities are more likely to be genuinely related than nodes with only sparse connections.

---

**Last Updated**: January 30, 2026  
**Status**: Active - core graph partitioning technique
