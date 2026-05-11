---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - complex_systems
  - social_networks
keywords:
  - clustering coefficient
  - local clustering coefficient
  - global clustering coefficient
  - transitivity
  - triadic closure
  - triangle density
  - network topology
  - Watts-Strogatz
  - graph clustering
topics:
  - Network Science
  - Graph Theory
  - Social Network Analysis
  - Complex Systems
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Clustering Coefficient

## Definition

The **clustering coefficient** is a measure of the degree to which nodes in a graph tend to cluster together, quantifying the prevalence of triangles (closed triplets) in a network. It captures the intuitive notion that "the friend of my friend is also my friend" -- a phenomenon known as **triadic closure** in social network analysis. The clustering coefficient ranges from 0 (no neighbors are connected to each other) to 1 (all neighbors form a complete subgraph, or clique).

Three principal formulations exist:

1. **Local clustering coefficient (C_i)**: For a node i with degree k_i, it measures the fraction of possible edges among i's neighbors that actually exist:

   C_i = 2 * T_i / (k_i * (k_i - 1))

   where T_i is the number of triangles containing node i. Equivalently, C_i is the number of edges among i's neighbors divided by the maximum possible edges among those neighbors. Nodes with degree 0 or 1 are conventionally assigned C_i = 0.

2. **Global clustering coefficient (transitivity)**: A network-level measure defined as the ratio of closed triplets to all connected triples:

   C_global = 3 * (number of triangles) / (number of connected triples)

   The factor of 3 accounts for the fact that each triangle contributes to three connected triples. This metric weights high-degree nodes more heavily because they participate in more triples.

3. **Average clustering coefficient**: The arithmetic mean of local clustering coefficients across all nodes:

   C_avg = (1/N) * sum(C_i for all i)

   This metric, introduced by Watts and Strogatz (1998), weights all nodes equally and thus gives more influence to low-degree nodes compared to the global transitivity measure.

## Historical Context

| Year | Contributor | Contribution |
|------|-------------|-------------|
| 1998 | Duncan Watts & Steven Strogatz | Formalized the clustering coefficient as a quantitative network metric in "Collective dynamics of 'small-world' networks" (*Nature*); showed real networks have C >> C_random |
| 1998 | Watts & Strogatz | Introduced the average clustering coefficient and used it alongside path length to define the small world property |
| 2004 | Barrat et al. | Proposed generalization of clustering coefficient to **weighted networks**, incorporating edge weights into the triangle count |
| 2005 | Onnela et al. | Developed an alternative weighted clustering coefficient using geometric mean of edge weights |
| 2007 | Fagiolo | Extended the clustering coefficient to **directed networks**, defining separate in-, out-, mid-, and cycle-based variants |
| 2018 | Clemente & Grassi | Unified framework for directed weighted clustering coefficients |

The concept has deep roots in sociology. **Triadic closure** -- the tendency for two people with a common friend to become friends themselves -- was identified as a fundamental social process long before the graph-theoretic formalization. The clustering coefficient provides the quantitative machinery to measure this effect across entire networks.

## Taxonomy

| Variant | Scope | Formula / Approach | Key Characteristic |
|---------|-------|-------------------|-------------------|
| **Local C_i (Watts-Strogatz)** | Single node | C_i = 2T_i / (k_i(k_i-1)) | Measures individual node's neighborhood density |
| **Global (Transitivity)** | Entire network | 3 * triangles / connected triples | Weights high-degree nodes more heavily |
| **Average C** | Entire network | Mean of all C_i | Weights all nodes equally; introduced by Watts-Strogatz |
| **Weighted (Barrat et al.)** | Single node | Incorporates edge weight strength s_i into triangle count | Captures intensity of connections, not just topology |
| **Weighted (Onnela et al.)** | Single node | Uses geometric mean of triangle edge weights | Normalizes by maximum weight to stay in [0,1] |
| **Directed (Fagiolo)** | Single node | Separate formulas for in/out/mid/cycle triangles | Distinguishes directionality of edges in triangle patterns |
| **Directed Weighted (Clemente-Grassi)** | Single node | Combines directional and weight information | Most general formulation for real-world networks |
| **Bipartite** | Two-mode network | Adapted for two-mode projections | Avoids inflation artifacts from projection |

## Key Properties

- **Range**: Always in [0, 1] for both local and global variants. C_i = 1 means all neighbors of node i are mutually connected; C_i = 0 means no two neighbors share an edge.
- **Triangle-based metric**: Fundamentally counts closed triangles relative to potential triangles (connected triples). It is a purely local structural measure.
- **Random graph baseline**: In Erdos-Renyi random graphs, the expected clustering coefficient is approximately C ~ p = <k>/N, where <k> is the average degree and N is the number of nodes. As N grows, C tends to 0 -- real networks deviate dramatically from this prediction.
- **Small world signature**: High clustering coefficient combined with short average path length (L ~ log N) is the defining quantitative signature of small world networks (Watts & Strogatz, 1998).
- **Degree-dependent clustering**: In many real-world networks, C(k) decreases with node degree k, often following C(k) ~ k^(-1). This pattern indicates hierarchical or modular organization.
- **Global vs. average discrepancy**: The global clustering coefficient (transitivity) and average clustering coefficient can differ substantially because they weight nodes differently. The transitivity measure is influenced more by high-degree hubs.
- **Invariance under graph complement**: The clustering coefficient of a graph's complement is generally not simply related to the original, making it a non-trivial structural descriptor.
- **Not monotone under edge addition**: Adding an edge can decrease a node's local clustering coefficient if the new neighbor is poorly connected to existing neighbors.
- **Computational complexity**: Computing all local clustering coefficients requires O(N * k_max^2) time in the worst case, where k_max is the maximum degree. Efficient matrix-based methods using adjacency matrix traces can compute triangle counts as Tr(A^3)/6.
- **Transitivity interpretation**: The global clustering coefficient equals the probability that two nodes sharing a common neighbor are themselves connected -- directly quantifying the strength of triadic closure.

## Notable Systems / Implementations

| System / Network | Clustering Coefficient | Equivalent Random Graph C | Domain |
|-----------------|----------------------|--------------------------|--------|
| **Film actor collaborations** | 0.79 | 0.00027 | Social network |
| **C. elegans neural network** | 0.28 | 0.05 | Neuroscience |
| **Western US power grid** | 0.080 | 0.005 | Infrastructure |
| **Facebook social graph** | ~0.16 | Much lower | Online social network |
| **WWW hyperlink network** | ~0.11 | Much lower | Information network |
| **Scientific collaboration networks** | 0.34-0.73 | ~0.001-0.01 | Academic social networks |

These values from Watts & Strogatz (1998) and subsequent studies consistently show that real-world networks have clustering coefficients orders of magnitude higher than their random graph counterparts.

## Applications

| Domain | Application | Clustering Coefficient Role |
|--------|------------|---------------------------|
| **Social network analysis** | Measuring social cohesion and trust | High clustering indicates tightly-knit social groups; triadic closure drives link prediction |
| **Community detection** | Identifying densely connected subgroups | Local clustering coefficient variation helps identify community boundaries; nodes with high C_i are likely within community cores |
| **Epidemiology** | Disease spread modeling | High clustering concentrates local outbreaks but can slow global epidemic spread compared to random mixing |
| **Neuroscience** | Brain network characterization | Brain networks exhibit high clustering supporting efficient local information processing |
| **Fraud and abuse detection** | Identifying coordinated behavior | Abnormally high or low clustering among account interaction graphs can indicate organized rings or synthetic networks |
| **Network evolution** | Temporal dynamics and growth models | Tracking clustering coefficient over time reveals how networks self-organize and form modular structures |
| **Link prediction** | Predicting future connections | Nodes sharing many common neighbors (high local clustering context) are more likely to form future links |

## Challenges and Limitations

### Measurement and Interpretation Challenges

- **Sensitivity to network size**: Comparing clustering coefficients across networks of different sizes requires careful normalization; raw C values can be misleading without controlling for density.
- **Disconnected components**: Nodes with degree 0 or 1 have undefined or zero clustering coefficients, which can skew the average in sparse networks.
- **Global vs. average ambiguity**: The two network-level measures (transitivity vs. average C) can give conflicting impressions of clustering. There is no consensus on which is "better" -- the choice depends on whether high-degree nodes should dominate the measure.

### Methodological Challenges

- **Weighted network extensions**: Multiple competing definitions exist (Barrat, Onnela, Zhang-Horvath), each capturing different aspects of weighted clustering. Results can differ substantially depending on the chosen variant.
- **Directed network complexity**: Directed graphs produce multiple triangle motifs (cycle, middleman, in-star, out-star), each requiring a separate clustering measure. The correct variant depends on the analytical question.
- **Temporal networks**: The standard clustering coefficient is static; extending it to temporal or dynamic networks (where edges appear and disappear) remains an active research area.
- **Bipartite projection artifacts**: Computing clustering on a one-mode projection of a bipartite network inflates the coefficient; dedicated bipartite clustering measures are needed but less widely implemented.

### Theoretical Limitations

- **Not sufficient for network characterization**: Two networks can have identical clustering coefficients but very different topologies. The clustering coefficient captures only triangle density and ignores higher-order motifs.
- **Random graph inadequacy**: The Erdos-Renyi model's failure to produce realistic clustering (C ~ p -> 0 as N -> infinity) motivated configuration models and stochastic block models, but generating graphs with prescribed clustering remains computationally challenging.

## Related Terms

- **[Small World Network](term_small_world_network.md)**: Small world networks are defined by simultaneously high clustering coefficient and short average path length; C is one of the two defining metrics
- **[Random Graph](term_random_graph.md)**: Erdos-Renyi random graphs serve as the null model baseline for clustering coefficient; real networks deviate dramatically from C_random ~ p
- **[Degree Distribution](term_degree_distribution.md)**: Degree-dependent clustering C(k) reveals hierarchical structure; the degree distribution determines the baseline expectation for clustering
- **[Network Centrality](term_network_centrality.md)**: Centrality and clustering measure different structural aspects; high-centrality nodes (bridges) often have lower local clustering than peripheral nodes
- **[Community Detection](term_community_detection.md)**: Dense intra-community connections produce high local clustering; clustering coefficient variation helps identify community boundaries
- **[Graph](term_graph.md)**: The fundamental data structure on which clustering coefficient is defined; requires understanding of adjacency, degree, and paths
- **[Power Law](term_power_law.md)**: Scale-free networks with power-law degree distributions often exhibit degree-dependent clustering C(k) ~ k^(-1), linking the two concepts
- **[Adjacency Matrix](term_adjacency_matrix.md)**: Triangle counts (and thus clustering coefficients) can be computed via Tr(A^3)/6 using the adjacency matrix
- **[Graph Laplacian](term_graph_laplacian.md)**: Spectral methods related to the graph Laplacian provide alternative views of local connectivity structure
- **[GNN - Graph Neural Networks](term_gnn.md)**: Message-passing in GNNs is influenced by local clustering; high clustering affects over-smoothing behavior

## References

### Vault Sources

### External Sources
- [Watts, D.J. & Strogatz, S.H. (1998). "Collective dynamics of 'small-world' networks." *Nature*, 393(6684), 440-442](https://www.nature.com/articles/30918) — Original paper formalizing the clustering coefficient and establishing the small world network framework
- [Barrat, A. et al. (2004). "The architecture of complex weighted networks." *PNAS*, 101(11), 3747-3752](https://www.pnas.org/doi/10.1073/pnas.0400087101) — Generalization of clustering coefficient to weighted networks
- [Fagiolo, G. (2007). "Clustering in complex directed networks." *Physical Review E*, 76(2), 026107](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.76.026107) — Extension to directed networks with multiple triangle motif types
- [Onnela, J.-P. et al. (2005). "Intensity and coherence of motifs in weighted complex networks." *Physical Review E*, 71(6), 065103](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.71.065103) — Alternative weighted clustering coefficient using geometric mean of weights
- [GeeksforGeeks: Clustering Coefficient in Graph Theory](https://www.geeksforgeeks.org/dsa/clustering-coefficient-graph-theory/) — Accessible tutorial with formulas and examples
- [Math Insight: Clustering Coefficient Definition](https://mathinsight.org/definition/clustering_coefficient) — Concise formal definition with mathematical notation
- [Wikipedia: Clustering Coefficient](https://en.wikipedia.org/wiki/Clustering_coefficient) — Comprehensive reference with all variants and historical context

---

**Last Updated**: March 15, 2026
**Status**: Active — Network science, graph theory, and social network analysis
