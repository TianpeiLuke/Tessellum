---
tags:
 - entry_point
 - index
 - network_science
 - graph_theory
 - game_theory
 - social_networks
keywords:
 - network science glossary
 - graph theory
 - social network analysis
 - network formation
 - random graphs
 - preferential attachment
 - diffusion models
 - game theory on networks
topics:
 - Network Science
 - Graph Theory
 - Social Network Analysis
 - Game Theory
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Acronym Glossary — Network Science & Graph Theory

**Purpose**: Quick-reference glossary for network science, graph theory, and game theory on networks. Covers theoretical foundations (random graphs, strategic formation), structural properties (centrality, clustering, degree distributions), dynamics (diffusion, learning), and cooperative game theory on networks.

**Primary Source**: Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press.

**Related Glossaries**:
- [Statistics Glossary](acronym_glossary_statistics.md) — causal inference, experimental design, Bayesian methods
- [ML Glossary](acronym_glossary_ml.md) — graph neural networks (GNN, TGN, RGAT) that learn on network data
- [Cognitive Science Glossary](acronym_glossary_cognitive_science.md) — behavioral concepts (information cascades, game theory) that operate on networks

---

## Network Models & Formation

### Random Graph
**Full Name**: Random Graph (General Class)
**Description**: The family of probabilistic models for generating networks stochastically. **Random graph models serve as both null models (baselines for testing non-randomness) and generative models (mechanisms for network formation).** The taxonomy ranges from the simple Erdos-Renyi model through configuration models, stochastic block models, and ERGMs, each capturing progressively more realistic structural features. Jackson Ch 3-5 covers random graph theory as the foundation for understanding network formation.
**Documentation**: [Random Graph](../resources/term_dictionary/term_random_graph.md)
**Related**: [Erdos-Renyi Model](#erdos-renyi-model), [Poisson Random Graph](#poisson-random-graph), [Configuration Model](#configuration-model), [Stochastic Block Model](#stochastic-block-model)

### Erdos-Renyi Model
**Full Name**: Erdos-Renyi Model ($G(n,p)$ and $G(n,M)$)
**Description**: The foundational random graph model with two formulations: $G(n,p)$ includes each edge independently with probability $p$ (Gilbert 1959); $G(n,M)$ samples uniformly from graphs with exactly $M$ edges (Erdos-Renyi 1959). **Exhibits sharp phase transitions — a giant component emerges when average degree exceeds 1, and connectivity appears at $p = \ln(n)/n$.** Invaluable as a mathematical benchmark but cannot produce the hubs, clustering, or community structure observed in real networks.
**Documentation**: [Erdos-Renyi Model](../resources/term_dictionary/term_erdos_renyi_model.md)
**Related**: [Poisson Random Graph](#poisson-random-graph), [Giant Component](#giant-component), [Configuration Model](#configuration-model)

### Poisson Random Graph
**Full Name**: Poisson Random Graph (Sparse Erdos-Renyi Regime)
**Description**: The Erdos-Renyi $G(n,p)$ model in the sparse regime $p = c/(n-1)$, where vertex degrees converge to a Poisson distribution with mean $c$. **The canonical null model in network science — the maximally random network consistent with a given average degree.** Any structural property deviating from the Poisson random graph prediction is evidence of non-random organizing principles. The thin Poisson tail (no hubs) versus the fat power-law tail of real networks is the single most important empirical fact motivating modern network science.
**Documentation**: [Poisson Random Graph](../resources/term_dictionary/term_poisson_random_graph.md)
**Related**: [Erdos-Renyi Model](#erdos-renyi-model), [Degree Distribution](#degree-distribution), [Power Law](#power-law), [Configuration Model](#configuration-model)

### Preferential Attachment
**Full Name**: Preferential Attachment (Barabasi-Albert Model)
**Description**: A network growth mechanism where new nodes preferentially connect to existing nodes with high degree — "the rich get richer." **Produces the power law degree distributions observed in real social, biological, and technological networks.** Introduced by Barabasi and Albert (1999) as a generative model for scale-free networks. Explains why a few hub nodes have vastly more connections than average.
**Documentation**: [Preferential Attachment](../resources/term_dictionary/term_preferential_attachment.md)
**Related**: [Random Graph](#random-graph), [Degree Distribution](#degree-distribution), [Power Law](../resources/term_dictionary/term_power_law.md)

### Configuration Model
**Full Name**: Configuration Model (Random Graph with Fixed Degree Sequence)
**Description**: A random graph model that generates networks with a **prescribed degree sequence** — each node is assigned a fixed number of half-edges ("stubs") that are then randomly paired to form edges. **The key null model for testing whether observed network properties (clustering, community structure, correlations) are explained by the degree distribution alone or require additional mechanisms.** Introduced by Bender and Canfield (1978), formalized by Molloy and Reed (1995). Unlike Erdos-Renyi (which fixes edge probability), the configuration model reproduces the fat-tailed degree distributions of real networks while randomizing all other structure.
**Documentation**: [Configuration Model](../resources/term_dictionary/term_configuration_model.md)
**Related**: [Random Graph](#random-graph), [Degree Distribution](#degree-distribution), [Stochastic Block Model](#stochastic-block-model)

### Price Model
**Full Name**: Price Model (Cumulative Advantage for Citation Networks)
**Description**: A directed network growth model where new nodes attach to existing nodes with probability proportional to their current in-degree plus a constant — **the first mathematical formalization of "cumulative advantage" (rich get richer) in networks.** Introduced by Derek de Solla Price (1965, 1976) to explain the power law distribution of citations in scientific literature. **Price's model preceded the Barabasi-Albert model by over two decades** and is the true origin of preferential attachment in network science. The directed nature makes it more appropriate for citation, web link, and information flow networks.
**Documentation**: [Price Model](../resources/term_dictionary/term_price_model.md)
**Related**: [Preferential Attachment](#preferential-attachment), [Power Law](#power-law), [Degree Distribution](#degree-distribution)

### ERGM
**Full Name**: Exponential Random Graph Model (p* Model)
**Description**: A statistical model for network formation that specifies the probability of observing a network as an exponential function of sufficient statistics (e.g., number of edges, triangles, k-stars). **The dominant approach for statistical inference on networks**, capturing local structural dependencies (reciprocity, transitivity, homophily) that Erdos-Renyi and configuration models cannot. Developed by Frank and Strauss (1986) and Wasserman and Pattison (1996). Jackson covers ERGMs in Ch 3 and Ch 13 as the primary tool for fitting models to observed network data.
**Documentation**: [ERGM](../resources/term_dictionary/term_ergm.md)
**Related**: [Random Graph](#random-graph), [Configuration Model](#configuration-model), [Homophily](#homophily)

### Stochastic Block Model
**Full Name**: Stochastic Block Model (SBM / Planted Partition Model)
**Description**: A generative random graph model where nodes are partitioned into groups (blocks) and edge probabilities depend only on the group memberships of the two endpoints. **The canonical probabilistic model for networks with community structure.** Introduced by Holland, Laskey, and Leinhardt (1983). Within-group edge probability is higher than between-group, generating the modular structure observed in real social and economic networks. Provides the theoretical foundation for community detection algorithms.
**Documentation**: [Stochastic Block Model](../resources/term_dictionary/term_stochastic_block_model.md)
**Related**: [Community Detection](#community-detection), [Random Graph](#random-graph), [Configuration Model](#configuration-model), [ERGM](#ergm)

### Pairwise Stability
**Full Name**: Pairwise Stability (Jackson-Wolinsky Equilibrium)
**Description**: A game-theoretic equilibrium concept for network formation where no agent wants to sever an existing link and no pair of unlinked agents both want to add a link. **Introduced by Jackson and Wolinsky (1996) as the foundational stability concept for strategic network formation.** Reveals a fundamental tension: efficient networks (maximizing total welfare) are often not pairwise stable, and stable networks are often not efficient — paralleling classic public goods problems.
**Documentation**: [Pairwise Stability](../resources/term_dictionary/term_pairwise_stability.md)
**Related**: [Shapley Value](#shapley-value), [Game Theory](../resources/term_dictionary/term_game_theory.md)

### Small World Network
**Full Name**: Small World Network (Watts-Strogatz Model)
**Description**: A network that simultaneously exhibits high clustering (friends of friends tend to be friends) and short average path length (any two nodes can be reached in few steps). **Formalized by Watts and Strogatz (1998) to explain the "six degrees of separation" phenomenon.** Generated by rewiring a small fraction of links in a regular lattice. Explains how information and disease can spread rapidly through locally clustered populations.
**Documentation**: [Small World Network](../resources/term_dictionary/term_small_world_network.md)
**Related**: [Random Graph](#random-graph), [Clustering Coefficient](#clustering-coefficient), [HNSW](../resources/term_dictionary/term_hnsw.md)

### Giant Component
**Full Name**: Giant Component (Phase Transition in Random Graphs)
**Description**: A connected subgraph containing a constant fraction of all nodes in the network. **In Erdos-Renyi random graphs, a giant component emerges sharply when the average degree exceeds 1** — one of the most celebrated results in random graph theory. Below this threshold, the network consists of many small isolated components; above it, a single giant component absorbs most nodes while small components persist. This phase transition is analogous to percolation in physics and has direct implications for epidemic thresholds, network resilience, and the viability of diffusion processes.
**Documentation**: [Giant Component](../resources/term_dictionary/term_giant_component.md)
**Related**: [Random Graph](#random-graph), [SIR Model](#sir-model), [SIS Model](#sis-model), [Degree Distribution](#degree-distribution)

### Phase Transition
**Full Name**: Phase Transition in Random Graph Theory
**Description**: An abrupt qualitative change in the structural properties of a random graph as a parameter crosses a critical value — the probability of a property jumps from 0 to 1 over a vanishingly narrow window. **The giant component transition at mean degree $c = 1$ is the most celebrated example**: below this threshold all components have $O(\log n)$ vertices; above it, a unique giant component absorbs a macroscopic fraction of the network. The connectivity threshold at $p = \ln(n)/n$ marks when isolated vertices disappear. Mathematically equivalent to bond percolation on the complete graph, phase transitions connect random graph theory to statistical physics and explain when networks "work" (giant component enables diffusion) versus "fail" (fragmentation under attack).
**Documentation**: [Phase Transition](../resources/term_dictionary/term_phase_transition_random_graphs.md)
**Related**: [Erdos-Renyi Model](#erdos-renyi-model), [Giant Component](#giant-component), [Poisson Random Graph](#poisson-random-graph)

### Percolation Theory (Networks)
**Full Name**: Percolation Theory on Networks
**Description**: A framework from statistical physics that studies connectivity of networks when edges (bond percolation) or nodes (site percolation) are removed with some probability. **Scale-free networks are robust to random failure but catastrophically fragile to targeted hub removal** (Albert, Jeong, Barabasi 2000). The percolation threshold $p_c = \langle k \rangle / (\langle k^2 \rangle - \langle k \rangle)$ is the critical fraction at which the giant component disintegrates. Newman (2002) established that SIR epidemic dynamics map exactly to bond percolation, connecting outbreak size to giant component size. Generating function methods (Newman, Strogatz, Watts 2001) provide exact analytical solutions for arbitrary degree distributions.
**Documentation**: [Percolation Theory (Networks)](../resources/term_dictionary/term_percolation_theory_networks.md)
**Related**: [Giant Component](#giant-component), [Phase Transition](#phase-transition), [SIR Model](#sir-model), [Power Law](#power-law), [Configuration Model](#configuration-model)

---

## Foundational Structures

### Graph
**Full Name**: Graph (Network)
**Description**: A mathematical structure consisting of nodes (vertices) and edges (links) that model pairwise relationships between entities. **The foundational data structure of network science** — every concept in this glossary (centrality, clustering, community detection, random graphs, diffusion, game theory on networks) operates on graphs. Key variants include directed/undirected, weighted/unweighted, bipartite, heterogeneous (multiple node/edge types), temporal (time-evolving), and hypergraphs (edges connecting 3+ nodes). The adjacency matrix $A$ and graph Laplacian $L = D - A$ are the two matrix representations that enable spectral analysis.
**Documentation**: [Graph](../resources/term_dictionary/term_graph.md)
**Related**: [Adjacency Matrix](#adjacency-matrix), [Graph Laplacian](#graph-laplacian), [DAG](#dag---directed-acyclic-graph), [GNN](acronym_glossary_ml.md#gnn---graph-neural-networks), [Random Graph](#random-graph), [Knowledge Graph](../resources/term_dictionary/term_knowledge_graph.md)

### DAG - Directed Acyclic Graph
**Full Name**: DAG — Directed Acyclic Graph
**Description**: A graph with directed edges (arrows) and no cycles, used to represent causal assumptions, dependency structures, and information flow. Three junction types determine information flow: **chain** (A→B→C, mediator), **fork** (A←B→C, confounder), and **collider** (A→B←C). Controlling for a variable blocks chains and forks but *opens* colliders — a counterintuitive property that explains many selection biases. Originates from Sewall Wright's path analysis (1920s), formalized by Pearl. DAGs are also foundational in scheduling, topological sorting, and Bayesian networks.
**Documentation**: [Directed Acyclic Graph](../resources/term_dictionary/term_directed_acyclic_graph.md)
**Related**: [Graph](#graph), [Adjacency Matrix](#adjacency-matrix), [Structural Causal Model](acronym_glossary_statistics.md#structural-causal-model), [Confounding Variable](acronym_glossary_statistics.md#confounding-variable)

---

## Spectral Graph Theory

### Spectral Graph Theory
**Full Name**: Spectral Graph Theory
**Description**: The study of graphs through the eigenvalues and eigenvectors of matrices associated with them — primarily the adjacency matrix $A$ and the graph Laplacian $L = D - A$. **Spectral methods reveal global graph structure (connectivity, clustering, community structure) from algebraic properties of these matrices.** The eigenvalues encode fundamental graph properties: the largest eigenvalue of $A$ determines epidemic thresholds, the second-smallest eigenvalue of $L$ (algebraic connectivity) determines how well-connected the graph is, and the eigenvectors provide optimal graph partitions. Foundation for spectral clustering, community detection, graph signal processing, and convergence analysis of diffusion processes.
**Documentation**: [Spectral Graph Theory](../resources/term_dictionary/term_spectral_graph_theory.md)
**Related**: [Graph Laplacian](#graph-laplacian), [Adjacency Matrix](#adjacency-matrix), [Algebraic Connectivity](#algebraic-connectivity), [Spectral Clustering](#spectral-clustering), [Eigenvector Centrality](#eigenvector-centrality)

### Adjacency Matrix
**Full Name**: Adjacency Matrix
**Description**: The $n \times n$ matrix $A$ where entry $A_{ij} = 1$ if nodes $i$ and $j$ are connected and $0$ otherwise (for unweighted graphs). **The fundamental algebraic representation of a graph** that enables spectral analysis, matrix operations, and computational algorithms. The largest eigenvalue $\lambda_1$ determines the SIS epidemic threshold ($1/\lambda_1$); the leading eigenvector gives eigenvector centrality; powers $A^k$ count walks of length $k$ between nodes. Symmetric for undirected graphs. Generalizes to weighted adjacency matrices where $A_{ij}$ is the edge weight.
**Documentation**: [Adjacency Matrix](../resources/term_dictionary/term_adjacency_matrix.md)
**Related**: [Graph Laplacian](#graph-laplacian), [Graph](#graph), [Eigenvector Centrality](#eigenvector-centrality), [SIS Model](#sis-model)

### Graph Laplacian
**Full Name**: Graph Laplacian ($L = D - A$)
**Description**: The matrix $L = D - A$ where $D$ is the diagonal degree matrix and $A$ is the adjacency matrix. **The central object of spectral graph theory** — its eigenvalues and eigenvectors encode the graph's connectivity, community structure, and diffusion properties. Always positive semidefinite with smallest eigenvalue 0 (multiplicity equals the number of connected components). The second-smallest eigenvalue (algebraic connectivity / Fiedler value) measures how well-connected the graph is. The normalized Laplacian $\mathcal{L} = D^{-1/2}LD^{-1/2}$ is used in spectral clustering. DeGroot learning convergence and random walk mixing times are both governed by the Laplacian spectrum.
**Documentation**: [Graph Laplacian](../resources/term_dictionary/term_graph_laplacian.md)
**Related**: [Adjacency Matrix](#adjacency-matrix), [Algebraic Connectivity](#algebraic-connectivity), [Spectral Clustering](#spectral-clustering), [DeGroot Learning](#degroot-learning)

### Eigenvector Centrality
**Full Name**: Eigenvector Centrality (Bonacich Centrality)
**Description**: A centrality measure where a node's importance is proportional to the sum of the centralities of its neighbors — **being connected to well-connected nodes matters more than simply having many connections.** Defined as the leading eigenvector of the adjacency matrix $A$: $Ax = \lambda_1 x$. Jackson (Ch 2) identifies eigenvector centrality as the measure determining long-run influence in DeGroot learning: as agents repeatedly average neighbors' beliefs, each agent's weight in the converged opinion equals their eigenvector centrality. PageRank is a regularized variant that adds a damping factor to handle disconnected graphs and dangling nodes.
**Documentation**: [Eigenvector Centrality](../resources/term_dictionary/term_eigenvector_centrality.md)
**Related**: [Network Centrality](#network-centrality), [PPR](#ppr---personalized-pagerank), [Adjacency Matrix](#adjacency-matrix), [DeGroot Learning](#degroot-learning)

### Algebraic Connectivity
**Full Name**: Algebraic Connectivity (Fiedler Value / Spectral Gap)
**Description**: The second-smallest eigenvalue $\lambda_2$ of the graph Laplacian $L$, also known as the Fiedler value. **Measures how well-connected a graph is** — larger $\lambda_2$ means harder to disconnect by removing edges. Zero if and only if the graph is disconnected. The corresponding eigenvector (Fiedler vector) provides the optimal bisection of the graph, used in spectral clustering. In economics, Golub and Jackson (2012) showed that $\lambda_2$ determines the rate of convergence in DeGroot learning — calling it the network's "spectral homophily." The Cheeger inequality relates $\lambda_2$ to the graph's conductance (minimum normalized edge cut).
**Documentation**: [Algebraic Connectivity](../resources/term_dictionary/term_algebraic_connectivity.md)
**Related**: [Graph Laplacian](#graph-laplacian), [Spectral Clustering](#spectral-clustering), [Spectral Graph Theory](#spectral-graph-theory), [DeGroot Learning](#degroot-learning)

### Spectral Clustering
**Full Name**: Spectral Clustering
**Description**: A graph partitioning algorithm that uses the eigenvectors of the graph Laplacian to embed nodes into a low-dimensional space, then applies k-means clustering. **Provably approximates the optimal normalized graph cut** (Shi & Malik 2000, Ng, Jordan & Weiss 2001), finding clusters that minimize inter-cluster edges relative to cluster sizes. The key insight is that the bottom $k$ eigenvectors of the normalized Laplacian $\mathcal{L}$ naturally separate communities because the Fiedler vector already provides the optimal 2-way partition. Widely used in community detection, image segmentation, and dimensionality reduction. Connected to the Cheeger inequality, which guarantees the spectral partition quality.
**Documentation**: [Spectral Clustering](../resources/term_dictionary/term_spectral_clustering.md)
**Related**: [Community Detection](#community-detection), [Graph Laplacian](#graph-laplacian), [Algebraic Connectivity](#algebraic-connectivity), [Stochastic Block Model](#stochastic-block-model)

### GSP - Graph Signal Processing
**Full Name**: Graph Signal Processing
**Description**: The extension of classical signal processing (Fourier transforms, filtering, sampling) from regular domains (time series, images) to irregular graph domains using the graph Laplacian's eigenvectors as a frequency basis. **The Graph Fourier Transform (GFT) decomposes signals on nodes into spectral components**, where low-frequency components vary smoothly across edges and high-frequency components change rapidly between neighbors. Spectral filtering on graphs enables denoising, compression, and feature extraction on network data. GSP provides the theoretical foundation for spectral GNN architectures (ChebNet, GCN) — graph convolution IS spectral filtering. Pioneered by Shuman et al. (2013) and Sandryhaila & Moura (2013).
**Documentation**: [Graph Signal Processing](../resources/term_dictionary/term_graph_signal_processing.md)
**Related**: [Graph Laplacian](#graph-laplacian), [Spectral Graph Theory](#spectral-graph-theory), [Spectral Clustering](#spectral-clustering), [GNN](acronym_glossary_ml.md#gnn---graph-neural-networks)

---

## Network Measurement & Properties

### Assortative Mixing
**Full Name**: Assortative Mixing (Assortativity)
**Description**: A network mixing pattern where nodes preferentially connect to other nodes with similar properties, most commonly measured by degree. **Newman (2002, 2003) formalized the assortativity coefficient $r$ as the Pearson correlation of node degrees at either end of an edge, ranging from $-1$ (perfectly disassortative) to $+1$ (perfectly assortative).** Social networks are generally assortative (popular people connect to popular people), while technological and biological networks are generally disassortative (hubs connect to many low-degree nodes). Assortative networks are more robust to targeted hub removal because interconnected hubs provide redundant connectivity.
**Documentation**: [Assortative Mixing](../resources/term_dictionary/term_assortative_mixing.md)
**Related**: [Homophily](#homophily), [Degree Distribution](#degree-distribution), [Community Detection](#community-detection), [Configuration Model](#configuration-model)

### Degree Distribution
**Full Name**: Degree Distribution
**Description**: The probability distribution describing the number of connections (degree) each node has in a network. **The single most informative structural property of a network.** Real social and technological networks consistently exhibit fat-tailed (power law) degree distributions, meaning a few hub nodes have orders of magnitude more connections than the median — placing them firmly in Taleb's Extremistan. Erdos-Renyi models produce Poisson (thin-tailed) distributions; preferential attachment produces power law distributions.
**Documentation**: [Degree Distribution](../resources/term_dictionary/term_degree_distribution.md)
**Related**: [Preferential Attachment](#preferential-attachment), [Power Law](../resources/term_dictionary/term_power_law.md), [Fat Tails](../resources/term_dictionary/term_fat_tails.md)

### Network Centrality
**Full Name**: Network Centrality Measures
**Description**: A family of metrics quantifying the "importance" of a node in a network, each capturing a different dimension. **No single centrality measure suffices — the right choice depends on what "important" means in context.** Degree centrality (number of connections), betweenness centrality (fraction of shortest paths passing through), closeness centrality (average distance to all others), and eigenvector centrality (connected to other well-connected nodes). PageRank and PPR are descendants of eigenvector centrality.
**Documentation**: [Network Centrality](../resources/term_dictionary/term_network_centrality.md)
**Related**: [PPR](../resources/term_dictionary/term_ppr.md), [Degree Distribution](#degree-distribution)

### Homophily
**Full Name**: Homophily
**Description**: The tendency for individuals to form connections with others who are similar to themselves — "birds of a feather flock together." **The most robust empirical regularity in social network analysis and the primary confound in network causal inference.** When similar people cluster together, it becomes extremely difficult to distinguish genuine peer effects (behavior spreading through the network) from selection effects (similar people choosing each other). First formalized by Lazarsfeld and Merton (1954).
**Documentation**: [Homophily](../resources/term_dictionary/term_homophily.md)
**Related**: [Community Detection](../resources/term_dictionary/term_community_detection.md), [Information Cascades](../resources/term_dictionary/term_information_cascades.md)

### Clustering Coefficient
**Full Name**: Clustering Coefficient
**Description**: The proportion of a node's neighbors that are also connected to each other — a measure of "triadic closure" (if A knows B and C, how likely are B and C to know each other). **The key structural property that distinguishes real social networks from random graphs.** Real networks have clustering coefficients 10-100x higher than Erdos-Renyi random graphs of the same size and density. High clustering combined with short path lengths defines the small world property.
**Documentation**: [Clustering Coefficient](../resources/term_dictionary/term_clustering_coefficient.md)
**Related**: [Small World Network](#small-world-network), [Random Graph](#random-graph)

### Modularity
**Full Name**: Modularity ($Q$)
**Description**: A scalar quality function measuring the strength of a network's division into communities by comparing the fraction of within-community edges to the expected fraction under a configuration model null. **Introduced by Newman and Girvan (2004), modularity is the foundational objective function that launched community detection as a subfield of network science.** Defined as $Q = (1/2m) \sum [A_{ij} - k_i k_j / 2m] \delta(c_i, c_j)$, where higher values indicate stronger community structure. Subject to a resolution limit (Fortunato and Barthelemy 2007): communities smaller than $\sqrt{2m}$ may be undetectable. Modularity maximization is NP-hard, with the Louvain and Leiden algorithms as the dominant fast heuristics.
**Documentation**: [Modularity](../resources/term_dictionary/term_modularity.md)
**Related**: [Community Detection](#community-detection), [Configuration Model](#configuration-model), [Stochastic Block Model](#stochastic-block-model), [Spectral Clustering](#spectral-clustering)

### Community Detection
**Full Name**: Community Detection (Graph Partitioning / Modularity Optimization)
**Description**: The problem of identifying densely connected subgroups ("communities") within a network, where nodes within a community are more densely connected to each other than to nodes in other communities. **Formalizes the intuition that networks have modular structure** — social groups, functional modules, topic clusters. Key algorithms include Greedy Modularity Maximization (Newman 2004), Louvain method, spectral clustering, and label propagation. The modularity function Q measures quality of a partition relative to a null model. Central to anomaly ring detection: bad actors cluster with co-conspirators, and community detection separates these rings from the broader network.
**Documentation**: [Community Detection](../resources/term_dictionary/term_community_detection.md)
**Related**: [Clustering Coefficient](#clustering-coefficient), [Homophily](#homophily), [Network Centrality](#network-centrality), [Modularity](#modularity)

### PageRank
**Full Name**: PageRank
**Description**: The parent graph-importance algorithm whose stationary distribution under a damped random walk on the row-stochastic transition matrix scores each node by global authority. **Originally developed by Brin and Page (1998) to rank web pages by link structure**, PageRank is the basis for a family of variants (Personalized PageRank, Topic-Sensitive PageRank, TrustRank). Computed by power iteration; convergence governed by the spectral gap and guaranteed by the teleportation step that makes the walk irreducible and aperiodic. In the SlipBox, static PageRank was empirically shown to be ≈ in-degree on the vault corpus, motivating the production swap to a SQL `COUNT(*)` aggregate.
**Documentation**: [PageRank](../resources/term_dictionary/term_pagerank.md)
**Related**: [PPR](#ppr---personalized-pagerank), [Random Walk](#random-walk), [Eigenvector Centrality](#eigenvector-centrality), [Spectral Graph Theory](#spectral-graph-theory)

### Random Walk
**Full Name**: Random Walk on Graphs
**Description**: A stochastic process on a graph that visits nodes by following edges chosen probabilistically at each step. The long-run probability that the walker is at node *v* — the **stationary distribution** — encodes graph importance relative to the seeds: nodes reachable from the seeds via many short paths receive high mass. The teleportation parameter (1 − α) controls the trade-off between graph-following and restart, and is what guarantees a unique stationary distribution. Underlies PageRank, Personalized PageRank, DeepWalk, node2vec, Pixie, and random-walk-with-restart algorithms used across web search, recommendation, and knowledge-graph retrieval.
**Documentation**: [Random Walk](../resources/term_dictionary/term_random_walk.md)
**Related**: [PageRank](#pagerank), [PPR](#ppr---personalized-pagerank), [Markov Random Field](#markov-random-field), [Eigenvector Centrality](#eigenvector-centrality)

### PPR - Personalized PageRank
**Full Name**: Personalized PageRank
**Description**: A graph ranking algorithm that ranks nodes by relevance to a set of seed nodes via biased random walks. **The computational implementation of eigenvector centrality** — the theoretical measure Jackson identifies as determining long-run influence in networks. Introduced as PageRank by Brin and Page (1998) for web search, generalized to personalized/topic-sensitive variants by Haveliwala (2002). In network science, PPR quantifies a node's structural importance relative to a query: nodes reachable via many short paths from the seeds score highest. Used in the vault itself as `static_ppr_score` for note importance ranking.
**Documentation**: [PPR](../resources/term_dictionary/term_ppr.md)
**Related**: [PageRank](#pagerank), [Random Walk](#random-walk), [Network Centrality](#network-centrality), [Eigenvector Centrality](#eigenvector-centrality)

### Pixie - Pinterest's Monte Carlo Random Walk
**Full Name**: Pixie (Pinterest random-walk recommendation system)
**Description**: A production random-walk system Pinterest built to recommend 3+ billion items to 200+ million users in real time, introduced by Eksombatchai et al. (WWW 2018). **Approximates Personalized PageRank by running N independent Monte Carlo random walks from seed nodes**, each with restart probability `p` at every step, ranking candidates by visit-count frequency. No matrix algebra, no global precomputation — pure local traversal that parallelizes trivially. Complexity is `O(N × L)` per query, independent of graph size. In the slipbox vault, included as the `pixie_random_walk` strategy (S7) in the FZ 5e2b1a benchmark to serve as the **no-semantic-bias structural baseline** that establishes a lower bound for the random-walk family. The empirical result (Hit@5 = 0.235 synth / 0.337 SlipBot — losing badly to PPR variants seeded via dense retrieval) was the load-bearing evidence for the conclusion *"the signal lives in the seeds, not in the walk dynamics."*
**Documentation**: [Pixie Random Walk](../resources/term_dictionary/term_pixie_random_walk.md)
**Wiki**: [Eksombatchai et al. WWW 2018, arXiv:1711.07601](https://arxiv.org/abs/1711.07601)
**Slipbox Application**: Strategy S7 in [FZ 5e2b1a Priority Graph Search Benchmark](../archives/experiments/experiment_priority_graph_search_benchmark.md); diagnostic baseline that isolates seeding-strategy effect from walk-dynamics effect
**Key Benefits**: Trivially parallel; no global precomputation; latency bounded by walk length × walks-per-seed; pure-Python implementation in `scripts/retrieval_strategies/pixie_random_walk.py`
**Related**: [PPR](#ppr---personalized-pagerank), [PageRank](#pagerank), [Random Walk](#random-walk), [BFS](../resources/term_dictionary/term_bfs.md), [](../resources/term_dictionary/term_hipporag.md)

---

## Network Distributions & Scaling

### Power Law
**Full Name**: Power Law Distribution
**Description**: A functional relationship where one quantity varies as a power of another: $p(x) \propto x^{-\alpha}$. The defining characteristic is **scale invariance** — the distribution looks the same at every scale, producing "heavy tails" where extreme events are rare but far more probable than Gaussian models predict. Power laws unify several well-known distributions (Pareto, Zipf, Yule-Simon) and appear across physics, biology, economics, linguistics, and network science. **In networks, power law degree distributions are the signature of scale-free networks** generated by preferential attachment. The Clauset et al. (2009) critique showed that many empirically claimed power laws fail rigorous statistical tests.
**Documentation**: [Power Law Term](../resources/term_dictionary/term_power_law.md)
**Source**: Newman, M.E.J. (2005). "Power laws, Pareto distributions and Zipf's law"; Clauset, A. et al. (2009). "Power-law distributions in empirical data"
**Related**: [Degree Distribution](#degree-distribution), [Preferential Attachment](#preferential-attachment), [Fat Tails](#fat-tails), [Zipf's Law](#zipfs-law), [Pareto Principle](acronym_glossary_cognitive_science.md#pareto-principle-8020-rule)

### Fat Tails
**Full Name**: Fat Tails (Fat-Tailed Distribution)
**Description**: A probability distribution whose tails decay as a power law ($p(x) \propto x^{-\alpha}$) rather than exponentially, meaning extreme events occur far more frequently than Gaussian models predict. Fat-tailed distributions are a subset of heavy-tailed distributions and include the Pareto, Cauchy, Levy-stable, and Student's t families. **For tail index $\alpha \leq 2$, the variance is infinite, invalidating standard statistical tools** (means, standard deviations, confidence intervals, regression). In network science, fat tails in degree distributions mean a few hub nodes have orders of magnitude more connections than the median — placing network properties firmly in Taleb's Extremistan.
**Documentation**: [Fat Tails Term](../resources/term_dictionary/term_fat_tails.md)
**Related**: [Power Law](#power-law), [Degree Distribution](#degree-distribution), [Tail Risk](acronym_glossary_statistics.md#tail-risk), [Mediocristan and Extremistan](acronym_glossary_statistics.md#mediocristan-and-extremistan), [Black Swan](acronym_glossary_cognitive_science.md#black-swan)

### Zipf's Law
**Full Name**: Zipf's Law (Rank-Frequency Law)
**Description**: An empirical observation that in many types of data, the frequency of an item is inversely proportional to its rank: $f(r) \propto r^{-\alpha}$, where $\alpha \approx 1$ for natural language. Named after linguist George Kingsley Zipf (1902–1950), who systematized the pattern in word frequencies. **Zipf's law is the discrete rank-frequency form of a power law**, while the Pareto distribution is the continuous probability form — both describe the same fundamental imbalance. The pattern appears across word frequencies, city sizes, website traffic, and network degree distributions.
**Documentation**: [Zipf's Law Term](../resources/term_dictionary/term_zipfs_law.md)
**Source**: Zipf, G.K. (1949). *Human Behavior and the Principle of Least Effort*
**Related**: [Power Law](#power-law), [Degree Distribution](#degree-distribution), [Pareto Principle](acronym_glossary_cognitive_science.md#pareto-principle-8020-rule), [Scaling Law](../resources/term_dictionary/term_scaling_law.md)

---

## Network Dynamics & Learning

### Complex Contagion
**Full Name**: Complex Contagion
**Description**: A spreading process on networks where adoption of a behavior requires exposure from multiple independent sources, unlike simple contagion (SIR/SIS) where a single contact suffices. **The core mechanism is social reinforcement: clustering and community structure facilitate complex contagion (by providing redundant reinforcing ties) but hinder simple contagion (by trapping it locally).** Formalized by Centola and Macy (2007), who showed that weak ties that accelerate simple contagion actually impede complex contagion by diluting local reinforcement. Centola (2010) experimentally confirmed that health behaviors spread farther and faster in clustered networks than random networks. Applications include technology adoption, social movements, and coordinated anomaly spreading.
**Documentation**: [Complex Contagion](../resources/term_dictionary/term_complex_contagion.md)
**Related**: [Threshold Models](#threshold-models), [SIR Model](#sir-model), [SIS Model](#sis-model), [Community Detection](#community-detection), [Small World Network](#small-world-network)

### DeGroot Learning
**Full Name**: DeGroot Learning Model
**Description**: A model of opinion formation on networks where agents repeatedly update their beliefs by taking a weighted average of their neighbors' beliefs. **Shows that convergence to consensus depends on network connectivity, and that influence in the converged belief is proportional to eigenvector centrality — not expertise.** Introduced by DeGroot (1974). Provides a simple but powerful framework for understanding echo chambers, polarization, and the conditions under which the "wisdom of crowds" succeeds or fails.
**Documentation**: [DeGroot Learning](../resources/term_dictionary/term_degroot_learning.md)
**Related**: [Network Centrality](#network-centrality), [Information Cascades](../resources/term_dictionary/term_information_cascades.md), [Homophily](#homophily)

### Bayesian Learning on Networks
**Full Name**: Bayesian Learning on Networks
**Description**: A model of rational belief updating where agents observe neighbors' actions and use Bayes' rule to update their beliefs about an unknown state of the world. **Unlike DeGroot learning (which always converges to consensus), Bayesian learning can produce information cascades** — situations where rational agents ignore their private information and copy predecessors, causing the entire network to converge on a potentially incorrect belief. Introduced by Bikhchandani, Hirshleifer, and Welch (1992). Jackson's treatment shows how network topology determines whether crowds are wise or herds are blind.
**Documentation**: [Bayesian Learning on Networks](../resources/term_dictionary/term_bayesian_learning_on_networks.md)
**Related**: [DeGroot Learning](#degroot-learning), [Information Cascades](../resources/term_dictionary/term_information_cascades.md), [Peer Effects](#peer-effects)

### SIR Model
**Full Name**: SIR (Susceptible-Infected-Recovered) Epidemic Model
**Description**: A compartmental epidemic model where individuals transition from susceptible to infected to recovered with permanent immunity. **Epidemics are self-limiting — they burn out as the susceptible pool depletes.** The basic reproduction number $R_0 = \beta/\gamma$ determines whether an epidemic occurs. Newman (2002) showed that SIR dynamics map exactly to bond percolation on networks, connecting final epidemic size to the giant component. Kermack and McKendrick (1927) established the foundational framework.
**Documentation**: [SIR Model](../resources/term_dictionary/term_sir_model.md)
**Related**: [SIS Model](#sis-model), [Giant Component](#giant-component), [Threshold Models](#threshold-models), [Power Law](#power-law)

### SIS Model
**Full Name**: SIS (Susceptible-Infected-Susceptible) Epidemic Model
**Description**: A compartmental epidemic model where recovered individuals return to the susceptible pool — there is no permanent immunity, enabling endemic steady states. **Pastor-Satorras and Vespignani (2001) proved that on scale-free networks the SIS epidemic threshold vanishes: any disease with any positive transmission rate can become endemic**, because high-degree hubs sustain infection as persistent reservoirs. The threshold on a general network is $\lambda_c = 1/\lambda_1$ (inverse of the largest eigenvalue of the adjacency matrix).
**Documentation**: [SIS Model](../resources/term_dictionary/term_sis_model.md)
**Related**: [SIR Model](#sir-model), [Degree Distribution](#degree-distribution), [Power Law](#power-law), [Preferential Attachment](#preferential-attachment)

### Threshold Models
**Full Name**: Threshold Models of Collective Behavior (Granovetter Model)
**Description**: A model of cascading adoption on networks where each agent adopts a behavior when the fraction of their neighbors who have already adopted exceeds their individual threshold. **Introduced by Granovetter (1978) and formalized on networks by Jackson, Watts, and others.** Explains cascading failures, viral adoption, bank runs, and social tipping points. Unlike SIR/SIS models (which use probabilistic transmission), threshold models capture **strategic** adoption where agents respond to the prevalence of adoption in their neighborhood. The structure of the network determines whether a small seed of early adopters triggers a global cascade or fizzles out.
**Documentation**: [Threshold Models](../resources/term_dictionary/term_threshold_models.md)
**Related**: [SIR Model](#sir-model), [SIS Model](#sis-model), [Information Cascades](../resources/term_dictionary/term_information_cascades.md), [Peer Effects](#peer-effects), [Strategic Complementarity](#strategic-complementarity)

### Peer Effects
**Full Name**: Peer Effects (Social Influence / Endogenous Effects)
**Description**: The causal influence of a person's social contacts on their behavior, beliefs, or outcomes. **The central empirical challenge of network social science: distinguishing genuine peer effects from homophily (selection) and correlated effects (shared environment).** Manski (1993) identified the "reflection problem" — in a linear model, it is impossible to separately identify endogenous effects (behavior influenced by peers' behavior), exogenous effects (behavior influenced by peers' characteristics), and correlated effects (shared unobservables) without additional structure. Jackson emphasizes that network structure provides the identifying variation that Manski's framework lacks.
**Documentation**: [Peer Effects](../resources/term_dictionary/term_peer_effects.md)
**Related**: [Homophily](#homophily), [Bayesian Learning on Networks](#bayesian-learning-on-networks), [DeGroot Learning](#degroot-learning), [Threshold Models](#threshold-models)

---

## Network Game Theory & Allocation

### Shapley Value
**Full Name**: Shapley Value (and Myerson Value)
**Description**: A solution concept from cooperative game theory that assigns each player a payoff based on their marginal contribution across all possible coalitions. **The unique allocation rule satisfying efficiency, symmetry, dummy player, and additivity axioms.** Introduced by Lloyd Shapley (1953; Nobel Prize 2012). The Myerson value (1977) extends Shapley to networks by restricting cooperation to connected subgraphs — a player's payoff depends on their position in the network, not just their intrinsic value.
**Documentation**: [Shapley Value](../resources/term_dictionary/term_shapley_value.md)
**Related**: [Pairwise Stability](#pairwise-stability), [Game Theory](../resources/term_dictionary/term_game_theory.md)

### Network Externalities
**Full Name**: Network Externalities (Network Effects)
**Description**: The phenomenon where the value of a product, service, or network membership increases as more people use it. **Jackson's central insight is that link formation in networks creates externalities for third parties** — when two agents form a link, they reduce path lengths for everyone else, creating a public goods problem. This drives the fundamental efficiency-stability tension: individually rational link decisions produce socially suboptimal networks because agents don't internalize the benefits their connections create for others. Direct externalities (more users = more value, e.g. telephone) and indirect externalities (more users = more complementary goods, e.g. operating systems) both shape network structure.
**Documentation**: [Network Externalities](../resources/term_dictionary/term_network_externalities.md)
**Related**: [Pairwise Stability](#pairwise-stability), [Strategic Complementarity](#strategic-complementarity), [Shapley Value](#shapley-value)

### Strategic Complementarity
**Full Name**: Strategic Complementarity on Networks
**Description**: A property of games on networks where an agent's incentive to take an action **increases** when more of their neighbors take the same action. **Produces coordination problems and multiple equilibria** — the network can tip between high-adoption and low-adoption states. Examples include technology adoption (more neighbors using a platform increases your benefit), crime (more criminal neighbors reduce detection risk), and public goods provision (more contributors increase returns). The complement is **strategic substitutability**, where an agent's incentive decreases when neighbors act (e.g., security provision, where one neighbor's investment protects the whole neighborhood). Network topology determines which equilibria are reachable and how easily the network can be tipped between them.
**Documentation**: [Strategic Complementarity](../resources/term_dictionary/term_strategic_complementarity.md)
**Related**: [Threshold Models](#threshold-models), [Peer Effects](#peer-effects), [Network Externalities](#network-externalities), [Pairwise Stability](#pairwise-stability)

---

### CDK (domain) — Centralized Documented Knowledge
**Full Name**: Centralized Documented Knowledge
**Definition**: [term_cdk_knowledge](../resources/term_dictionary/term_cdk_knowledge.md) — domain shared knowledge control plane combining document stores + vector stores + knowledge graphs with unified metadata governance.
**Related**: [Knowledge Graph](../resources/term_dictionary/term_knowledge_graph.md), [Slipbox](../resources/term_dictionary/term_slipbox.md), [RAG](../resources/term_dictionary/term_rag.md)

### Scale-Free Network
**Definition**: [term_scale_free_network](../resources/term_dictionary/term_scale_free_network.md) — Network with power-law degree distribution (P(k) ~ k^-γ). Generated by preferential attachment. The Abuse Slipbox exhibits scale-free properties (α=1.4-1.8).
**Related**: [Power Law](../resources/term_dictionary/term_power_law.md), [Preferential Attachment](../resources/term_dictionary/term_preferential_attachment.md)

## Cross-Reference: Theory to Practice

| Theory Concept | Vault Application | Connection |
|---------------|-------------------|------------|
| Eigenvector centrality / PageRank | Vault PPR scoring (`static_ppr_score`) | Jackson's centrality theory IS the foundation of the vault's note importance ranking |
| Power law degree distributions | Abuse network detection | Fraud rings exhibit non-random degree distributions detectable by GNN models |
| Preferential attachment | Knowledge graph growth | High-PPR notes attract more links over time — the vault itself exhibits preferential attachment |
| Homophily | Abuse ring identification | Bad actors cluster with similar bad actors; community detection exploits this |
| Information cascades | Abuse technique propagation | New anomaly vectors spread through bad-actor networks via cascade dynamics |
| Small world property | Vault navigation | Short average path length means any two notes are ~3 hops apart despite local clustering |
| Assortative mixing | Abuse ring structure analysis | Fraud rings may exhibit anomalous assortativity patterns — degree correlations reveal coordinated account clusters |
| Complex contagion | Coordinated anomaly spreading | Abuse techniques require social reinforcement (multiple sources) to adopt — complex contagion dynamics explain why anomaly clusters in communities |

## Related Entry Points

- [Statistics Glossary](acronym_glossary_statistics.md) — causal inference, Mediocristan/Extremistan, tail risk, Bayesian inference
- [ML Glossary](acronym_glossary_ml.md) — GNN, TGN, graph neural network architectures
- [Cognitive Science Glossary](acronym_glossary_cognitive_science.md) — game theory, information cascades, behavioral economics

## References

- Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press.
- [Digest: Social and Economic Networks](../resources/digest/digest_social_economic_networks_jackson.md) — comprehensive digest of Jackson's book
- Barabasi, A.L. & Albert, R. (1999). "Emergence of Scaling in Random Networks." *Science*, 286(5439), 509-512.
- Watts, D.J. & Strogatz, S.H. (1998). "Collective Dynamics of 'Small-World' Networks." *Nature*, 393, 440-442.
- Erdos, P. & Renyi, A. (1959). "On Random Graphs." *Publicationes Mathematicae*, 6, 290-297.
