---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - social_network_analysis
keywords:
  - network centrality
  - centrality measure
  - degree centrality
  - betweenness centrality
  - closeness centrality
  - eigenvector centrality
  - PageRank
  - Katz centrality
  - Bonacich centrality
  - Freeman centrality
  - node importance
  - graph ranking
topics:
  - Network Science
  - Graph Theory
  - Social Network Analysis
  - Graph Algorithms
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Network Centrality

## Definition

**Network centrality** is a family of measures in graph theory and network analysis that assign numerical scores or rankings to nodes (vertices) in a graph, quantifying their structural importance or influence within the network. Centrality answers the question: *"What characterizes an important node?"* by providing a real-valued function on vertices whose values identify the most prominent, influential, or strategically positioned actors in a network.

Formally, a centrality measure is a function $C: V \to \mathbb{R}$ defined on the vertex set $V$ of a graph $G = (V, E)$, where higher values indicate greater importance according to a specific structural criterion. Different centrality measures capture different notions of importance -- a node may be "central" because it has many connections (degree), because it lies on many shortest paths (betweenness), because it is close to all other nodes (closeness), or because it is connected to other important nodes (eigenvector).

The concept is foundational to network science, with applications spanning social influence analysis, epidemiological modeling, information retrieval, transportation planning, and fraud detection. Hundreds of distinct centrality measures have been proposed, but four classical measures -- degree, betweenness, closeness, and eigenvector centrality -- form the core of the field.

## Historical Context

| Year | Contributor | Contribution |
|------|-----------|-------------|
| 1948 | Alex Bavelas | Introduced the concept of centrality in communication networks, linking node position to group efficiency |
| 1950 | Alex Bavelas | Formalized closeness-based centrality in small group experiments |
| 1953 | Leo Katz | Proposed Katz centrality, considering all paths (not just shortest) with exponential attenuation |
| 1954 | Marvin Shaw | Extended Bavelas's work on centrality and communication patterns |
| 1965 | Charles Hubbell | Developed matrix-based status scoring anticipating eigenvector centrality |
| 1972 | Phillip Bonacich | Defined eigenvector centrality as the principal eigenvector of the adjacency matrix |
| 1977 | Linton Freeman | Introduced betweenness centrality based on shortest-path intermediation |
| 1978/79 | Linton Freeman | Published the landmark paper "Centrality in Social Networks: Conceptual Clarification," unifying degree, closeness, and betweenness under a common framework |
| 1987 | Phillip Bonacich | Generalized eigenvector centrality with a tunable parameter for cooperative vs. competitive networks |
| 1998 | Brin & Page | Introduced PageRank for web search, a variant of eigenvector centrality with damping |

Freeman's 1978/79 paper in *Social Networks* is the single most influential work in the field, providing the conceptual and mathematical framework that unified previously disparate notions of centrality. It established the three classical measures (degree, closeness, betweenness) and introduced the concept of **graph centralization** -- a network-level measure of how concentrated centrality is around a single node.

## Taxonomy

### The Four Classical Centrality Measures

| Measure | Core Question | Formula (Unnormalized) | Captures |
|---------|--------------|----------------------|----------|
| **Degree** | How many connections does a node have? | $C_D(v) = \deg(v)$ | Local connectivity, activity |
| **Betweenness** | How often does a node lie on shortest paths? | $C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$ | Brokerage, control of flow |
| **Closeness** | How close is a node to all others? | $C_C(v) = \frac{1}{\sum_{t} d(v,t)}$ | Efficiency, independence |
| **Eigenvector** | Is a node connected to other important nodes? | $C_E(v) = \frac{1}{\lambda} \sum_{j \in N(v)} C_E(j)$ | Recursive influence, prestige |

Where $\sigma_{st}$ is the total number of shortest paths from $s$ to $t$, $\sigma_{st}(v)$ is the number of those paths passing through $v$, $d(v,t)$ is the geodesic distance from $v$ to $t$, and $\lambda$ is the largest eigenvalue of the adjacency matrix.

### Extended Centrality Measures

| Measure | Based On | Key Modification | Introduced By |
|---------|---------|-----------------|--------------|
| **Katz Centrality** | Eigenvector | Adds a bias term to all nodes; counts all walks with attenuation factor $\alpha$ | Katz (1953) |
| **PageRank** | Eigenvector | Divides influence by out-degree; adds damping factor for random restarts | Brin & Page (1998) |
| **Bonacich Power** | Eigenvector | Tunable parameter $\beta$: positive for cooperative, negative for competitive networks | Bonacich (1987) |
| **Harmonic Centrality** | Closeness | Uses sum of reciprocal distances instead of reciprocal of sum; handles disconnected graphs | Marchiori & Latora (2000) |
| **Percolation Centrality** | Betweenness | Weights paths by percolation states of source and target nodes | Piraveenan et al. (2013) |
| **Information Centrality** | Closeness | Based on information flow rather than geodesic distance | Stephenson & Zelen (1989) |

### Centrality Classification by What They Measure

| Category | Measures | What They Capture |
|----------|---------|------------------|
| **Volume-based** | Degree, Katz | How much direct or indirect connectivity a node has |
| **Distance-based** | Closeness, Harmonic, Information | How efficiently a node can reach or be reached by others |
| **Path-based** | Betweenness, Percolation, Flow | How much a node controls or mediates flow between others |
| **Spectral** | Eigenvector, PageRank, Bonacich | Recursive importance derived from neighbors' importance |

## Key Properties

- **Degree centrality** is the simplest and cheapest to compute ($O(n)$ for a single node), but captures only local structure; a node with high degree may be peripheral if all its neighbors are low-degree
- **Betweenness centrality** identifies brokers and gatekeepers who control information flow; high-betweenness nodes are critical for network connectivity and their removal can fragment the network
- **Closeness centrality** identifies nodes that can spread information most efficiently; it is sensitive to network disconnection (undefined for unreachable pairs unless harmonic variant is used)
- **Eigenvector centrality** captures the idea that "it matters not just how many connections you have, but who you are connected to"; it is the steady-state of a recursive status-assignment process
- **Katz centrality** solves the problem that eigenvector centrality assigns zero scores to nodes in directed acyclic graphs (DAGs) by adding a baseline prestige to every node
- **PageRank** treats influence as a finite resource: a node distributes its centrality equally among its out-neighbors, preventing nodes with many outgoing links from inflating all their targets' scores
- **Most centrality measures are positively correlated** in empirical networks, meaning they often (but not always) identify similar sets of important nodes; the divergence between measures is itself informative about network structure
- **Normalization** is required for cross-network comparison: degree is typically normalized by $(n-1)$, betweenness by $\frac{(n-1)(n-2)}{2}$, and closeness by $(n-1)$
- **Graph centralization** (Freeman, 1978) measures how much a network's centrality distribution resembles a star graph; a centralization score of 1.0 indicates a perfect star topology
- **Directed networks** require distinguishing in-centrality from out-centrality for degree, closeness, and betweenness; eigenvector centrality uses the left or right eigenvector depending on convention
- **Weighted networks** generalize all classical measures: degree becomes node strength (sum of edge weights), and shortest-path-based measures use weighted distances
- **Computational complexity** varies significantly: degree is $O(m)$ for all nodes, closeness is $O(nm)$ using BFS, betweenness is $O(nm)$ using Brandes' algorithm (2001), and eigenvector centrality requires iterative methods converging in $O(km)$ where $k$ is the number of iterations

## When to Use Which Measure

| Scenario | Best Measure | Rationale |
|----------|-------------|-----------|
| Identify most connected / popular nodes | Degree | Direct connections indicate activity and visibility |
| Find gatekeepers who control information flow | Betweenness | Nodes on many shortest paths can filter or distort information |
| Find nodes that can broadcast information fastest | Closeness | Short average distance means rapid dissemination |
| Identify nodes with influential friends | Eigenvector | Recursive prestige captures second-order influence |
| Rank web pages by authority | PageRank | Handles directed links and distributes authority proportionally |
| Rank nodes in directed acyclic graphs | Katz | Works where eigenvector centrality yields zero scores |
| Identify super-spreaders in an epidemic | Degree or Eigenvector | Epidemic spreading correlates with contact volume and contact quality |
| Find critical infrastructure nodes | Betweenness | Failure of high-betweenness nodes maximally disrupts connectivity |
| Analyze competitive exchange networks | Bonacich ($\beta < 0$) | In bargaining, power comes from being connected to weak (dependent) partners |
| Analyze cooperative social networks | Bonacich ($\beta > 0$) | In collaboration, power comes from being connected to other powerful actors |

## Notable Systems / Implementations

| System | Centrality Used | Application Domain |
|--------|----------------|-------------------|
| **Google Search (PageRank)** | PageRank (eigenvector variant) | Web page ranking and information retrieval |
| **NetworkX (Python)** | All classical + PageRank, Katz | General-purpose network analysis library |
| **igraph (R/Python/C)** | All classical + many variants | High-performance graph analysis |
| **SNAP (Stanford)** | All classical measures | Large-scale network analysis |
| **Gephi** | All classical + PageRank | Interactive network visualization and analysis |
| **Neo4j Graph Data Science** | Degree, betweenness, closeness, PageRank | Graph database analytics |
| **Amazon Nexus KG** | PPR (PageRank variant) | Knowledge graph ranking for fraud detection |
| **HippoRAG** | PPR (PageRank variant) | Knowledge graph retrieval for LLM systems |
| **Brandes' Algorithm** | Betweenness | $O(nm)$ exact betweenness for large networks (Brandes, 2001) |

## Applications

| Domain | Centrality Measures Used | Application |
|--------|------------------------|-------------|
| **Social Influence** | Degree, Eigenvector, PageRank | Identify opinion leaders, influential users, viral seed selection for marketing campaigns |
| **Epidemiology** | Degree, Betweenness, Eigenvector | Identify super-spreaders, vaccination targeting, contact tracing prioritization |
| **Information Retrieval** | PageRank, HITS | Web search ranking, citation analysis, academic impact assessment |
| **Transportation** | Betweenness, Closeness | Identify critical road intersections, optimize public transit, assess infrastructure vulnerability |
| **Neuroscience** | Degree, Betweenness, Eigenvector | Map brain connectivity hubs, identify critical neural pathways |
| **Fraud Detection** | PageRank (PPR), Degree | Rank suspicious accounts in fraud rings, propagate risk signals through account linkage graphs |
| **Counter-terrorism** | Betweenness, Degree | Identify key actors in covert networks, find communication bottlenecks |
| **Ecology** | Degree, Betweenness | Identify keystone species in food webs, assess ecosystem robustness |
| **Bibliometrics** | PageRank, Eigenvector | Journal impact ranking, author influence measurement, citation network analysis |
| **Organizational Design** | Closeness, Betweenness | Identify informal leaders, optimize communication structure, detect information silos |

## Challenges and Limitations

### Conceptual Challenges

- **No universal "best" centrality**: Different measures capture fundamentally different aspects of importance; the choice depends on what "importance" means in the specific context
- **Correlation vs. redundancy**: In many real networks, centrality measures are highly correlated, making it unclear whether using multiple measures adds analytical value
- **Static vs. dynamic networks**: Classical centrality is defined for static snapshots, but real networks evolve; temporal centrality measures remain an active research area

### Computational Challenges

- **Scalability**: Betweenness and closeness require all-pairs shortest paths ($O(nm)$), which is prohibitive for networks with millions of nodes; approximation algorithms (e.g., sampling-based betweenness) trade accuracy for speed
- **Disconnected graphs**: Closeness centrality is undefined for nodes in different components; harmonic centrality or component-wise normalization is needed
- **Directed acyclic graphs**: Eigenvector centrality assigns zero to all nodes in a DAG; Katz centrality or PageRank must be used instead

### Methodological Challenges

- **Normalization sensitivity**: Different normalization schemes can change relative rankings, especially when comparing across networks of different sizes
- **Edge weight interpretation**: Weights can represent connection strength (higher = better) or distance/cost (higher = worse); the choice affects closeness and betweenness calculations
- **Network boundary effects**: Centrality scores depend on where the network boundary is drawn; incomplete data can dramatically alter rankings
- **Stability**: Small perturbations in network structure (adding/removing a few edges) can significantly change betweenness and closeness rankings, while degree rankings are more robust

## Related Terms
- **[Personalized PageRank (PPR)](term_ppr.md)**: PageRank variant that biases random walks toward seed nodes; used in GraphRAG and knowledge graph retrieval
- **[Graph Neural Networks (GNN)](term_gnn.md)**: Deep learning on graphs; GNN message passing generalizes centrality-based aggregation to learned representations
- **[Power Law](term_power_law.md)**: Degree distributions in scale-free networks follow power laws, directly connecting to degree centrality distributions
- **[Directed Acyclic Graph (DAG)](term_directed_acyclic_graph.md)**: Graph structure where eigenvector centrality fails (yields all zeros), motivating Katz centrality
- **[Community Detection](term_community_detection.md)**: Complementary graph analysis task; centrality identifies important nodes while community detection identifies important groups
- **[HippoRAG](term_hipporag.md)**: Knowledge retrieval system using PPR (a centrality-based ranking) for graph-based retrieval augmented generation

## References

### Vault Sources

### External Sources
- [Freeman, L.C. (1978). "Centrality in Social Networks: Conceptual Clarification." *Social Networks*, 1, 215-239](https://www.sciencedirect.com/science/article/abs/pii/0378873378900217) -- The foundational paper unifying degree, closeness, and betweenness centrality
- [Bonacich, P. (1972). "Factoring and Weighting Approaches to Status Scores and Clique Identification." *Journal of Mathematical Sociology*, 2, 113-120](https://doi.org/10.1080/0022250X.1972.9989806) -- Introduced eigenvector centrality as the principal eigenvector of the adjacency matrix
- [Katz, L. (1953). "A New Status Index Derived from Sociometric Analysis." *Psychometrika*, 18(1), 39-43](https://doi.org/10.1007/BF02289026) -- Proposed Katz centrality counting all walks with exponential attenuation
- [Brin, S. & Page, L. (1998). "The Anatomy of a Large-Scale Hypertextual Web Search Engine." *Computer Networks*, 30, 107-117](https://doi.org/10.1016/S0169-7552(98)00110-X) -- Introduced PageRank for web search ranking
- [Brandes, U. (2001). "A Faster Algorithm for Betweenness Centrality." *Journal of Mathematical Sociology*, 25(2), 163-177](https://doi.org/10.1080/0022250X.2001.9990249) -- Efficient O(nm) algorithm for computing betweenness centrality
- [Borgatti, S.P. (2005). "Centrality and Network Flow." *Social Networks*, 27(1), 55-71](https://doi.org/10.1016/j.socnet.2004.11.008) -- Unified framework linking centrality measures to network flow models
- [Bavelas, A. (1950). "Communication Patterns in Task-Oriented Groups." *Journal of the Acoustical Society of America*, 22(6), 725-730](https://doi.org/10.1121/1.1906679) -- Early experimental work establishing centrality in communication networks
- [Wikipedia: Centrality](https://en.wikipedia.org/wiki/Centrality) -- Comprehensive overview of centrality measures and their mathematical definitions
- [Cambridge Intelligence: Social Network Analysis 101](https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/) -- Practical guide to choosing between centrality measures
