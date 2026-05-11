---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - linear_algebra
  - spectral_methods
keywords:
  - eigenvector centrality
  - eigencentrality
  - prestige score
  - Bonacich centrality
  - principal eigenvector
  - adjacency matrix eigenvector
  - Perron-Frobenius
  - power iteration
  - alpha-centrality
  - Katz-Bonacich centrality
topics:
  - Network Science
  - Graph Theory
  - Social Network Analysis
  - Spectral Methods
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Eigenvector Centrality

## Definition

**Eigenvector centrality** (also called eigencentrality or prestige score) is a measure of node influence in a network based on the principle that a node's importance is determined by the importance of its neighbors. Unlike degree centrality, which simply counts connections, eigenvector centrality assigns higher scores to nodes connected to other high-scoring nodes, capturing the recursive structure of influence in a network.

Formally, given a graph $G = (V, E)$ with adjacency matrix $A$, the eigenvector centrality $x_i$ of node $i$ is defined by:

$$x_i = \frac{1}{\lambda_1} \sum_{j} a_{ij} x_j$$

or equivalently in matrix form:

$$A \mathbf{x} = \lambda_1 \mathbf{x}$$

where $\mathbf{x}$ is the eigenvector associated with the **largest eigenvalue** $\lambda_1$ of the adjacency matrix $A$. The requirement that $\mathbf{x}$ be the leading eigenvector -- rather than any eigenvector -- is what guarantees all centrality scores are non-negative, a property ensured by the **Perron-Frobenius theorem** for connected graphs with non-negative adjacency matrices.

The self-referential nature of the definition (a node is important if its neighbors are important) is resolved precisely by the eigenvector equation: the eigenvector of the largest eigenvalue is the unique fixed point of this recursive definition. This is the centrality measure treated in Jackson (2008), Chapter 2, as part of the foundational toolkit for representing and measuring networks.

## Historical Context

| Year | Contributor | Contribution |
|------|-----------|-------------|
| 1941 | Wassily Leontief | Input-output economic models using matrix eigenvalue methods; anticipated the mathematical framework |
| 1949 | John Seeley | Early use of matrix-based status scoring in sociometric analysis |
| 1953 | Leo Katz | Proposed Katz centrality, counting all walks with exponential attenuation factor $\alpha$ -- a direct precursor |
| 1972 | Phillip Bonacich | Formally defined eigenvector centrality as the principal eigenvector of the adjacency matrix in "Factoring and Weighting Approaches to Status Scores and Clique Identification" |
| 1987 | Phillip Bonacich | Generalized to "power centrality" with tunable parameter $\beta$ in "Power and Centrality: A Family of Measures," unifying eigenvector and Katz centrality |
| 1998 | Brin & Page | Introduced PageRank, a regularized variant of eigenvector centrality with damping factor for web search |

Bonacich's 1972 paper is the foundational reference. His key insight was that a unit's status in a social network should depend not merely on the number of its connections but on the status of those connections -- a fundamentally recursive notion that the eigenvector of the adjacency matrix uniquely captures. The 1987 paper extended this by introducing a parameter $\beta$ that controls whether connections to powerful neighbors increase ($\beta > 0$, cooperative settings) or decrease ($\beta < 0$, competitive/bargaining settings) a node's centrality.

## Taxonomy

| Variant | Formula | Key Modification | Use Case |
|---------|---------|-----------------|----------|
| **Eigenvector Centrality** (Bonacich, 1972) | $A\mathbf{x} = \lambda_1 \mathbf{x}$ | Leading eigenvector of $A$ | Undirected, connected networks |
| **Katz Centrality** (Katz, 1953) | $\mathbf{x} = \alpha A \mathbf{x} + \mathbf{1}$ | Adds baseline prestige $\mathbf{1}$ to every node; attenuation $\alpha < 1/\lambda_1$ | DAGs and directed networks where eigenvector centrality yields zeros |
| **Bonacich Power Centrality** (Bonacich, 1987) | $\mathbf{c}(\alpha, \beta) = \alpha (I - \beta A)^{-1} A \mathbf{1}$ | Tunable $\beta$: positive for cooperative, negative for competitive | Bargaining and exchange networks |
| **Alpha-Centrality** (Bonacich & Lloyd, 2001) | $\mathbf{x} = \alpha A^T \mathbf{x} + \mathbf{e}$ | Generalization for directed graphs with exogenous status $\mathbf{e}$ | Asymmetric relations, citation networks |
| **PageRank** (Brin & Page, 1998) | $\mathbf{x} = d \hat{A} \mathbf{x} + \frac{(1-d)}{n} \mathbf{1}$ | Row-normalizes $A$; damping factor $d$ adds random jumps | Web search, knowledge graphs |

The relationship between these variants is hierarchical: eigenvector centrality is the limiting case of Katz centrality as $\alpha \to 1/\lambda_1$, and PageRank can be understood as eigenvector centrality applied to a regularized, row-normalized adjacency matrix with a teleportation component.

## Key Properties

- **Perron-Frobenius guarantee**: For connected, undirected graphs (irreducible, non-negative adjacency matrix), the Perron-Frobenius theorem guarantees that the largest eigenvalue $\lambda_1$ is real, positive, and simple, and the corresponding eigenvector has strictly positive entries. This ensures eigenvector centrality is well-defined and unique (up to scaling).
- **Recursive definition**: A node's centrality is proportional to the sum of its neighbors' centralities -- the eigenvector equation is the self-consistent solution to this recursion.
- **Power iteration computation**: Eigenvector centrality is computed via power iteration: start with an arbitrary positive vector $\mathbf{x}^{(0)}$, repeatedly compute $\mathbf{x}^{(k+1)} = A \mathbf{x}^{(k)}$ and normalize. Convergence rate depends on the eigenvalue gap $|\lambda_1 / \lambda_2|$; larger gaps mean faster convergence. NetworkX's implementation uses this method.
- **Connection to DeGroot learning**: In the DeGroot model of opinion dynamics, agents iteratively average their neighbors' beliefs using a trust matrix $T$. The long-run influence of each agent on the consensus belief is given by the left eigenvector of $T$ -- which is precisely the eigenvector centrality of the trust network. This means eigenvector centrality measures "who ultimately shapes group opinion."
- **Connection to PageRank**: PageRank is a regularized form of eigenvector centrality that (1) normalizes by out-degree so influence is divided among outgoing links, and (2) adds a damping/teleportation factor to ensure convergence on arbitrary directed graphs. As the damping factor $d \to 1$, PageRank approaches eigenvector centrality on strongly connected graphs.
- **Failure on directed acyclic graphs**: Eigenvector centrality assigns zero to all nodes in a DAG because there is no self-consistent assignment of positive scores without cycles. Katz centrality and PageRank resolve this by adding exogenous prestige.
- **Sensitivity to high-degree hubs**: In networks with heavy-tailed degree distributions, eigenvector centrality tends to concentrate on nodes in the largest hub neighborhood, sometimes making it less discriminating than betweenness or closeness for identifying non-hub important nodes.
- **Comparison with other centrality measures**: Degree centrality is local (counts only direct connections); closeness centrality measures geodesic efficiency; betweenness centrality measures brokerage on shortest paths. Eigenvector centrality uniquely captures "who you know matters" -- second-order and higher-order influence propagated through the entire network.

## Notable Systems / Implementations

| System | Implementation | Application |
|--------|---------------|-------------|
| **NetworkX** (`eigenvector_centrality`) | Power iteration with configurable tolerance and max iterations | General-purpose Python network analysis |
| **igraph** (`eigenvector_centrality`) | ARPACK-based eigensolver | High-performance graph analysis in R/Python/C |
| **Neo4j Graph Data Science** | Pregel-based distributed eigenvector centrality | Graph database analytics at scale |
| **Google PageRank** | Modified eigenvector centrality with damping on web graph | Web search ranking (the original "killer app") |
| **SNAP (Stanford)** | C++ eigenvector centrality for large networks | Academic large-scale network analysis |

## Applications

| Domain | Application | Mechanism |
|--------|------------|-----------|
| **Social influence analysis** | Identify opinion leaders and influential users | High eigenvector centrality = connected to other influential people |
| **Web search (PageRank)** | Rank web pages by authority | Pages linked by other authoritative pages rank higher |
| **Epidemiology** | Identify super-spreaders in contact networks | Nodes connected to other well-connected nodes amplify epidemic spread |
| **Economics (Leontief)** | Input-output analysis of economic sectors | Sector importance depends on importance of sectors it supplies |
| **Citation analysis** | Measure journal or paper influence | A citation from an influential journal counts more than one from an obscure journal |
| **Social learning (DeGroot)** | Determine long-run influence on group consensus | Eigenvector centrality of trust network = who shapes final beliefs |

## Challenges and Limitations

- **Disconnected graphs**: Eigenvector centrality is only well-defined for connected graphs. In disconnected networks, the leading eigenvector concentrates entirely on the largest component, assigning zero to all nodes in other components.
- **Directed graphs**: For directed graphs, left and right eigenvectors differ, and the choice between in-centrality and out-centrality must be made deliberately. Strongly connected components are required for non-trivial results.
- **DAG problem**: As noted, eigenvector centrality yields all zeros on DAGs. Katz centrality or alpha-centrality must be used instead.
- **Localization in scale-free networks**: In networks with extreme degree heterogeneity, eigenvector centrality can "localize" on the hub and its immediate neighborhood, reducing its discriminatory power for the rest of the network.
- **Computational convergence**: Power iteration convergence is slow when the eigenvalue gap $|\lambda_1 - \lambda_2|$ is small (i.e., when the spectral gap is narrow), which occurs in certain network topologies like barbell graphs.

## Related Terms
- **[Network Centrality](term_network_centrality.md)**: The parent family of measures; eigenvector centrality is one of the four classical centrality measures alongside degree, betweenness, and closeness
- **[PageRank](term_pagerank.md)**: Eigenvector centrality of the row-stochastic transition matrix with damping; the canonical retrieval-system instance of this measure
- **[Personalized PageRank (PPR)](term_ppr.md)**: A node-specific variant of PageRank (itself a regularized eigenvector centrality), used in knowledge graph retrieval and graph-based recommendation
- **[Random Walk](term_random_walk.md)**: The stochastic process whose stationary distribution coincides with the dominant eigenvector of the transition matrix
- **[DeGroot Learning](term_degroot_learning.md)**: Opinion dynamics model where the long-run influence vector equals the eigenvector centrality of the trust network
- **[Graph](term_graph.md)**: The fundamental mathematical structure on which eigenvector centrality is defined
- **[Power Law](term_power_law.md)**: Degree distributions following power laws interact with eigenvector centrality through localization effects in scale-free networks
- **[Knowledge Graph](term_knowledge_graph.md)**: Graph structures where PageRank and PPR (eigenvector centrality descendants) are used for entity ranking and retrieval

## References

### Vault Sources
- [Digest: Social and Economic Networks (Jackson, 2008)](../digest/digest_social_economic_networks_jackson.md) -- Chapter 2 introduces eigenvector centrality as part of the foundational toolkit for network measurement; Chapter 8 connects it to DeGroot learning influence

### External Sources
- [Bonacich, P. (1972). "Factoring and Weighting Approaches to Status Scores and Clique Identification." *Journal of Mathematical Sociology*, 2(1), 113-120.](https://doi.org/10.1080/0022250X.1972.9989806) -- The foundational paper defining eigenvector centrality
- [Bonacich, P. (1987). "Power and Centrality: A Family of Measures." *American Journal of Sociology*, 92(5), 1170-1182.](https://doi.org/10.1086/228631) -- Generalized eigenvector centrality with tunable parameter for cooperative vs. competitive networks
- [Katz, L. (1953). "A New Status Index Derived from Sociometric Analysis." *Psychometrika*, 18(1), 39-43.](https://doi.org/10.1007/BF02289026) -- Precursor to eigenvector centrality; counts all walks with attenuation
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch. 2.](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) -- Textbook treatment of eigenvector centrality within the broader framework of network measurement
- [Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.](https://global.oup.com/academic/product/networks-9780198805090) -- Comprehensive graduate-level treatment of eigenvector centrality and spectral methods
- [Bonacich, P. & Lloyd, P. (2001). "Eigenvector-like Measures of Centrality for Asymmetric Relations." *Social Networks*, 23(3), 191-201.](https://doi.org/10.1016/S0378-8733(01)00038-7) -- Introduced alpha-centrality for directed graphs
- [Wikipedia: Eigenvector Centrality](https://en.wikipedia.org/wiki/Eigenvector_centrality) -- Overview with mathematical formulation and properties
- [NetworkX: eigenvector_centrality](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.eigenvector_centrality.html) -- Reference implementation using power iteration

---

**Last Updated**: 2026-03-15
**Status**: Active -- important centrality measure covered by Jackson Ch 2; foundational to PageRank, DeGroot influence, and spectral network analysis
