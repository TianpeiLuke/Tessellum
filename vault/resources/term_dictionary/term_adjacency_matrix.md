---
tags:
  - resource
  - terminology
  - graph_theory
  - linear_algebra
  - network_science
  - matrix_theory
keywords:
  - adjacency matrix
  - graph matrix
  - A_{ij}
  - graph representation
  - spectral radius
  - graph eigenvalues
  - walk counting
  - symmetric matrix
  - weighted adjacency matrix
topics:
  - Graph Theory
  - Linear Algebra
  - Network Science
  - Spectral Methods
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Adjacency Matrix

## Definition

The **adjacency matrix** of a finite graph $G = (V, E)$ with $n = |V|$ vertices is an $n \times n$ square matrix $A$ whose entry $A_{ij}$ encodes the relationship between vertex $i$ and vertex $j$. For a **simple, unweighted, undirected graph**, the entry is binary:

$$A_{ij} = \begin{cases} 1 & \text{if } \{i, j\} \in E \\ 0 & \text{otherwise} \end{cases}$$

For a **directed graph** (digraph), $A_{ij} = 1$ if there is a directed edge from vertex $i$ to vertex $j$, and the matrix need not be symmetric. For a **weighted graph**, $A_{ij} = w_{ij}$ where $w_{ij}$ is the weight of the edge between $i$ and $j$ (or zero if no edge exists). Self-loops, when permitted, appear as nonzero diagonal entries.

The adjacency matrix is one of the most fundamental objects in graph theory and network science, serving as the bridge between combinatorial graph structure and linear algebra. Its algebraic properties — eigenvalues, eigenvectors, matrix powers — reveal deep structural information about the underlying graph, including connectivity, centrality, community structure, and dynamical behavior of processes running on the network.

## Historical Context

The adjacency matrix formalization emerged alongside the development of modern graph theory in the mid-20th century. While matrix representations of graphs appeared implicitly in earlier work on combinatorics and circuit theory, the systematic study of the adjacency matrix and its spectrum was pioneered by mathematicians and physicists in the 1950s-1970s.

The spectral theory of adjacency matrices was substantially advanced by Sachs (1964), who related graph structure to the characteristic polynomial, and by Cvetkovic, Doob, and Sachs in their 1980 monograph *Spectra of Graphs*. The modern treatment in algebraic graph theory was consolidated by Godsil and Royle (2001) in *Algebraic Graph Theory*, which remains the standard reference. On the applied side, Newman (2010) in *Networks: An Introduction* established the adjacency matrix as the central analytical tool for network science, connecting its spectral properties to centrality measures, epidemic thresholds, and diffusion processes.

## Taxonomy

| Variant | Entry $A_{ij}$ | Symmetry | Diagonal | Use Case |
|---------|----------------|----------|----------|----------|
| **Simple undirected** | $\{0, 1\}$ | Symmetric ($A = A^T$) | Zero (no self-loops) | Basic graph algorithms |
| **Directed (digraph)** | $\{0, 1\}$ | Generally asymmetric | Zero or $\{0,1\}$ | Web graphs, citation networks |
| **Weighted undirected** | $w_{ij} \in \mathbb{R}_{\geq 0}$ | Symmetric | Application-dependent | Correlation networks, distance graphs |
| **Weighted directed** | $w_{ij} \in \mathbb{R}_{\geq 0}$ | Generally asymmetric | Application-dependent | Flow networks, trust networks |
| **Signed** | $w_{ij} \in \{-1, 0, +1\}$ | Symmetric or asymmetric | Zero | Social balance theory, friend/foe networks |
| **Multigraph** | $k_{ij} \in \mathbb{N}_0$ (edge count) | Symmetric for undirected | $\geq 0$ | Parallel edges in transport networks |

## Key Properties

- **Symmetry for undirected graphs**: If $G$ is undirected, then $A = A^T$, making $A$ a real symmetric matrix. All eigenvalues are real, and eigenvectors can be chosen to be orthonormal. This is the foundation for spectral graph theory.
- **Powers count walks**: The $(i,j)$-entry of $A^k$ equals the number of walks of length $k$ from vertex $i$ to vertex $j$. This is one of the most important properties of the adjacency matrix, connecting combinatorial enumeration to matrix algebra.
- **Spectrum and eigenvalues**: The multiset of eigenvalues $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n$ of $A$ is called the **spectrum** of the graph. For an undirected graph, all eigenvalues are real. The trace of $A^k$ equals $\sum_i \lambda_i^k$, linking spectral information to walk counts.
- **Spectral radius**: The spectral radius $\rho(A) = \max_i |\lambda_i|$ equals the largest eigenvalue $\lambda_1$ for connected graphs with non-negative entries (by the Perron-Frobenius theorem). For a $d$-regular graph, $\lambda_1 = d$.
- **Perron-Frobenius theorem**: For a connected graph (irreducible adjacency matrix), the largest eigenvalue $\lambda_1$ is positive, simple, and has a corresponding eigenvector with all positive entries. This theorem guarantees the existence and uniqueness of eigenvector centrality for connected networks.
- **Eigenvector centrality**: The leading eigenvector $\mathbf{v}_1$ (corresponding to $\lambda_1$) assigns a centrality score to each vertex proportional to the sum of the centralities of its neighbors: $A\mathbf{v}_1 = \lambda_1 \mathbf{v}_1$. This is the mathematical basis for eigenvector centrality and the precursor to PageRank.
- **SIS epidemic threshold**: For the susceptible-infected-susceptible (SIS) epidemic model on a network, the epidemic threshold under mean-field approximation is $\tau_c = 1/\lambda_1$, where $\lambda_1$ is the spectral radius of $A$. Below this effective infection rate, the disease dies out; above it, it persists endemically. The spectral radius thus quantifies the network's vulnerability to epidemics.
- **Degree information**: The degree of vertex $i$ equals the $i$-th row sum: $d_i = \sum_j A_{ij}$. For undirected graphs, this also equals the $i$-th column sum.
- **Space complexity**: $O(n^2)$ storage regardless of the number of edges, making it inefficient for sparse graphs but enabling $O(1)$ edge existence queries.
- **Number of triangles**: The trace of $A^3$ counts $6 \times$ the number of triangles in an undirected graph (each triangle is counted once per vertex, once per direction).

## Comparison with Other Representations

| Representation | Definition | Space | Edge Query | Neighbor Iteration | Primary Use |
|---------------|-----------|-------|------------|-------------------|-------------|
| **Adjacency matrix** $A$ | $n \times n$ matrix, $A_{ij}$ = edge indicator/weight | $O(n^2)$ | $O(1)$ | $O(n)$ | Spectral analysis, dense graphs, matrix algebra |
| **Adjacency list** | Array of neighbor lists per vertex | $O(n + m)$ | $O(\deg)$ | $O(\deg)$ | Traversal, sparse graphs, most algorithms |
| **Edge list** | List of $(i, j)$ pairs (or triples for weighted) | $O(m)$ | $O(m)$ | $O(m)$ | I/O, streaming, edge-centric computation |
| **Incidence matrix** $B$ | $n \times m$ matrix, $B_{ve}$ = 1 if vertex $v$ incident to edge $e$ | $O(nm)$ | $O(m)$ | $O(m)$ | Flow problems, cycle space, Kirchhoff's laws |
| **Graph Laplacian** $L = D - A$ | Degree matrix minus adjacency matrix | $O(n^2)$ | N/A | N/A | Diffusion, clustering, graph partitioning, consensus |

The adjacency matrix is preferred when spectral methods are needed or when the graph is dense. For sparse graphs ($m \ll n^2$), adjacency lists are more memory-efficient. The graph Laplacian $L = D - A$ and its normalized variants are closely related to $A$ and are often preferred for diffusion, random walks, and clustering applications because $L$ is positive semidefinite with a clear spectral gap interpretation.

## Applications

| Domain | Application | Role of Adjacency Matrix |
|--------|------------|-------------------------|
| **Network science** | Centrality computation | Eigenvector centrality from leading eigenvector of $A$ |
| **Epidemiology** | SIS/SIR epidemic thresholds | Spectral radius $\lambda_1$ determines epidemic threshold $\tau_c = 1/\lambda_1$ |
| **Social learning** | DeGroot opinion dynamics | Trust matrix (row-normalized $A$) governs belief convergence |
| **Web search** | PageRank and PPR | Modified adjacency matrix of the web graph with damping |
| **Spectral clustering** | Community detection | Eigenvectors of $A$ (or $L$) identify cluster structure |
| **Quantum chemistry** | Huckel molecular orbital theory | Adjacency matrix of molecular graph predicts orbital energies |
| **Combinatorics** | Walk and path enumeration | $A^k$ counts length-$k$ walks between vertex pairs |

## Challenges and Limitations

- **Space inefficiency for sparse graphs**: Real-world networks (social, biological, technological) are typically sparse with $m = O(n)$ edges, but the adjacency matrix uses $O(n^2)$ space regardless. For networks with millions of nodes, explicit storage of $A$ is impractical.
- **Non-uniqueness under relabeling**: The adjacency matrix depends on vertex labeling. Two isomorphic graphs can have different adjacency matrices, and determining isomorphism from adjacency matrices is computationally hard (graph isomorphism problem).
- **Limited expressiveness for multigraphs and hypergraphs**: The standard adjacency matrix cannot naturally represent hyperedges (edges connecting more than two vertices) and collapses parallel edges into a single count or weight.
- **Spectral limitations**: Co-spectral graphs (non-isomorphic graphs with identical spectra) demonstrate that the eigenvalue spectrum does not uniquely determine graph structure. The spectrum alone is an incomplete invariant.
- **Computational cost of eigendecomposition**: Full eigendecomposition of an $n \times n$ matrix is $O(n^3)$, limiting exact spectral methods to moderate-sized networks. Iterative methods (Lanczos, power iteration) provide the leading eigenvalues efficiently but not the full spectrum.

## Related Terms

- **[Graph](term_graph.md)**: The combinatorial object that the adjacency matrix represents; $G = (V, E)$ defines the structure encoded in $A$
- **[Graph Laplacian](term_graph_laplacian.md)**: The matrix $L = D - A$ derived from the adjacency matrix and the degree matrix; preferred for diffusion and clustering applications
- **[Spectral Graph Theory](term_spectral_graph_theory.md)**: The study of graph properties through the eigenvalues and eigenvectors of associated matrices, primarily $A$ and $L$
- **[Eigenvector Centrality](term_eigenvector_centrality.md)**: A centrality measure defined by the leading eigenvector of the adjacency matrix, guaranteed by the Perron-Frobenius theorem
- **[SIS Model](term_sis_model.md)**: Susceptible-infected-susceptible epidemic model whose network threshold is $1/\lambda_1(A)$
- **[DeGroot Learning](term_degroot_learning.md)**: Opinion dynamics model where agents update beliefs via a row-stochastic trust matrix derived from the network's adjacency structure
- **[PPR (Personalized PageRank)](term_ppr.md)**: A random-walk-based centrality measure computed from a modified adjacency matrix with teleportation
- **[Network Centrality](term_network_centrality.md)**: Broader family of node importance measures, many of which are defined through the adjacency matrix or its transformations
- **[Random Graph](term_random_graph.md)**: Probabilistic graph models whose adjacency matrices have well-studied spectral properties (e.g., Wigner semicircle law for Erdos-Renyi)

## References

### Vault Sources

- [Digest: Social and Economic Networks (Jackson, 2008)](../digest/digest_social_economic_networks_jackson.md) — Chapter 2 introduces the adjacency matrix formalism; later chapters use spectral properties for centrality and learning dynamics

### External Sources

- [Godsil, C. & Royle, G. (2001). *Algebraic Graph Theory*. Springer Graduate Texts in Mathematics, Vol. 207.](https://doi.org/10.1007/978-1-4613-0163-9) — Definitive reference for the spectral theory of adjacency matrices, including Perron-Frobenius, interlacing, and strongly regular graphs
- [Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.](https://doi.org/10.1093/acprof:oso/9780199206650.001.0001) — Standard network science textbook; Chapter 6 covers the adjacency matrix, centrality, and spectral methods
- [Cvetkovic, D., Doob, M., & Sachs, H. (1980). *Spectra of Graphs: Theory and Applications*. Academic Press.](https://doi.org/10.1007/978-3-642-93486-6) — Foundational monograph on graph spectra, characteristic polynomials, and spectral characterization
- [Wang, Y. et al. (2003). "Epidemic Spreading in Real Networks: An Eigenvalue Viewpoint." *IEEE SRDS*.](https://doi.org/10.1109/RELDIS.2003.1238052) — Establishes that the epidemic threshold for SIS on networks is $1/\lambda_1$ of the adjacency matrix
- [Wikipedia: Adjacency Matrix](https://en.wikipedia.org/wiki/Adjacency_matrix) — Overview of definition, properties, and variants
- [Wolfram MathWorld: Adjacency Matrix](https://mathworld.wolfram.com/AdjacencyMatrix.html) — Concise formal definition and enumerative properties

---

**Last Updated**: 2026-03-15
**Status**: Active — foundational concept in graph theory, linear algebra, and network science
