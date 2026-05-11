---
tags:
  - resource
  - terminology
  - spectral_graph_theory
  - linear_algebra
  - network_science
  - matrix_theory
keywords:
  - graph Laplacian
  - Laplacian matrix
  - Kirchhoff matrix
  - admittance matrix
  - normalized Laplacian
  - signless Laplacian
  - spectral graph theory
  - positive semidefinite
  - algebraic connectivity
  - Fiedler vector
  - graph Fourier transform
topics:
  - Spectral Graph Theory
  - Linear Algebra
  - Network Science
  - Graph Signal Processing
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Graph Laplacian

## Definition

The **graph Laplacian** (also called the Laplacian matrix, Kirchhoff matrix, or admittance matrix) is a matrix representation of a graph that encodes its combinatorial structure through the difference between the degree matrix and the adjacency matrix. For an undirected graph $G = (V, E)$ with $n = |V|$ vertices, the **(combinatorial) graph Laplacian** is the $n \times n$ matrix:

$$L = D - A$$

where $D = \text{diag}(d_1, d_2, \ldots, d_n)$ is the diagonal **degree matrix** with $D_{ii} = \deg(v_i)$, and $A$ is the **adjacency matrix** with $A_{ij} = 1$ if $(v_i, v_j) \in E$ and $0$ otherwise. Element-wise, the Laplacian is:

$$L_{ij} = \begin{cases} \deg(v_i) & \text{if } i = j \\ -1 & \text{if } i \neq j \text{ and } (v_i, v_j) \in E \\ 0 & \text{otherwise} \end{cases}$$

The graph Laplacian is the discrete analogue of the continuous Laplace operator $\nabla^2$ from differential geometry. Just as the continuous Laplacian measures how a function deviates from its local average, the graph Laplacian measures how a signal on a vertex deviates from the average signal on its neighbors. This connection makes it the fundamental operator for studying diffusion, smoothness, and connectivity on discrete structures.

For weighted graphs, the definition generalizes naturally: $A_{ij} = w_{ij}$ for edge weight $w_{ij}$, and $D_{ii} = \sum_j w_{ij}$ (the weighted degree).

## Historical Context

The graph Laplacian has roots in Gustav Kirchhoff's 1847 work on electrical networks, where he used it to formulate his circuit laws and prove the **Matrix-Tree Theorem** — the result that the number of spanning trees of a graph equals any cofactor of the Laplacian matrix. For this reason, the matrix is sometimes called the *Kirchhoff matrix*.

The term "Laplacian" derives from Pierre-Simon Laplace (1786), who studied the continuous Laplace operator in celestial mechanics. The graph-theoretic version was recognized as a discrete analogue much later, as algebraic graph theory developed in the 20th century.

Despite Kirchhoff's early contribution, the graph Laplacian did not receive sustained attention until **Miroslav Fiedler**'s seminal papers in 1973 and 1975. Fiedler introduced the concept of *algebraic connectivity* — the second-smallest eigenvalue $\lambda_2$ of $L$ — and showed that the corresponding eigenvector (the *Fiedler vector*) encodes information about graph partitioning and connectivity. This work laid the foundation for spectral graph partitioning.

| Year | Contributor | Contribution |
|------|------------|--------------|
| 1847 | Gustav Kirchhoff | Introduced the matrix for electrical networks; Matrix-Tree Theorem |
| 1973-75 | Miroslav Fiedler | Algebraic connectivity ($\lambda_2$); Fiedler vector for graph partitioning |
| 1989 | Bojan Mohar | Systematic study of Laplacian eigenvalues; Cheeger-type inequalities for graphs |
| 1991 | Bojan Mohar | "The Laplacian Spectrum of Graphs" — comprehensive survey |
| 1997 | Fan Chung | *Spectral Graph Theory* monograph; normalized Laplacian theory |
| 2001 | Shi & Malik | Normalized cuts using graph Laplacian for image segmentation |
| 2007 | Ulrike von Luxburg | "A Tutorial on Spectral Clustering" — unified treatment for machine learning |
| 2013 | Shuman, Narang, Frossard, Ortega, Vandergheynst | Foundational paper on graph signal processing |

## Taxonomy

The graph Laplacian has several important variants, each suited to different analytical tasks.

### Laplacian Variants

| Variant | Definition | Key Property | Primary Use |
|---------|-----------|--------------|-------------|
| **Combinatorial Laplacian** $L$ | $D - A$ | Eigenvalues depend on vertex degrees | Counting spanning trees, connectivity |
| **Symmetric Normalized Laplacian** $\mathcal{L}$ | $D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}$ | Eigenvalues in $[0, 2]$; degree-independent | Spectral clustering, graph Fourier transform |
| **Random-Walk Laplacian** $L_{\text{rw}}$ | $D^{-1} L = I - D^{-1} A = I - P$ | Left eigenvectors = stationary distribution | Random walks, diffusion, DeGroot learning |
| **Signless Laplacian** $Q$ | $D + A$ | Positive semidefinite; smallest eigenvalue $= 0$ iff bipartite | Bipartiteness detection, signed graphs |

### Relationship Between Variants

The three main Laplacian forms are related by similarity transformations:
- $\mathcal{L} = D^{-1/2} L \, D^{-1/2}$, so $\mathcal{L}$ and $L_{\text{rw}}$ share eigenvalues
- If $\mathbf{v}$ is an eigenvector of $\mathcal{L}$, then $D^{-1/2} \mathbf{v}$ is an eigenvector of $L_{\text{rw}}$
- $L_{\text{rw}} = I - P$, where $P = D^{-1}A$ is the random walk transition matrix
- The combinatorial Laplacian $L$ has the same null space as the other variants, but its nonzero eigenvalues are degree-dependent

### Weighted and Directed Extensions

For **weighted graphs**, replace binary adjacency with edge weights: $A_{ij} = w_{ij}$, and $D_{ii} = \sum_j w_{ij}$.

For **directed graphs**, one typically uses the *in-degree* or *out-degree* Laplacian, though the theory is substantially more complex since symmetry is lost. Chung (2005) developed a normalized Laplacian for directed graphs using the Perron vector of the transition matrix.

## Key Properties

- **Positive semidefiniteness**: $L$ is positive semidefinite (all eigenvalues $\lambda_i \geq 0$). This follows directly from the quadratic form (see below).

- **Quadratic form**: For any signal $\mathbf{x} \in \mathbb{R}^n$, the Laplacian quadratic form equals:
$$\mathbf{x}^\top L \mathbf{x} = \sum_{(i,j) \in E} (x_i - x_j)^2$$
This measures the total "roughness" or "Dirichlet energy" of the signal $\mathbf{x}$ on the graph. It is zero if and only if $\mathbf{x}$ is constant on each connected component.

- **Smallest eigenvalue is always zero**: The vector $\mathbf{1} = (1, 1, \ldots, 1)^\top$ is always an eigenvector of $L$ with eigenvalue $0$, since each row of $L$ sums to zero.

- **Multiplicity of eigenvalue 0 equals the number of connected components**: If $G$ has $k$ connected components, then $\lambda_1 = \lambda_2 = \cdots = \lambda_k = 0$ and $\lambda_{k+1} > 0$. The null space of $L$ is spanned by the indicator vectors of each connected component.

- **Algebraic connectivity**: The second-smallest eigenvalue $\lambda_2(L)$, also called the *Fiedler value* or *algebraic connectivity*, measures how well-connected the graph is. $\lambda_2 > 0$ if and only if $G$ is connected. Larger $\lambda_2$ means the graph is harder to disconnect.

- **Kirchhoff's Matrix-Tree Theorem**: The number of spanning trees of $G$ equals any cofactor of $L$, or equivalently:
$$\tau(G) = \frac{1}{n} \prod_{i=2}^{n} \lambda_i$$
where $\lambda_2, \ldots, \lambda_n$ are the nonzero eigenvalues of $L$.

- **Spectrum bounds**: For the combinatorial Laplacian, $0 = \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n \leq 2 \cdot d_{\max}$. For the normalized Laplacian, eigenvalues lie in $[0, 2]$, with $\lambda_n = 2$ if and only if $G$ has a bipartite component.

- **Symmetry**: $L$ is real symmetric for undirected graphs, guaranteeing real eigenvalues and orthogonal eigenvectors.

- **Singular**: $L$ always has a nontrivial null space (rank at most $n - 1$ for a connected graph), so it is never invertible. The **pseudoinverse** $L^+$ is used instead and relates to effective resistance and commute times.

- **Cheeger inequality**: The algebraic connectivity $\lambda_2$ is related to the Cheeger constant (isoperimetric number) $h(G)$ by:
$$\frac{h(G)^2}{2 d_{\max}} \leq \lambda_2 \leq 2 h(G)$$
This links spectral and combinatorial notions of expansion.

- **Interlacing**: Adding or removing edges changes Laplacian eigenvalues in a controlled way (Cauchy interlacing theorem), enabling perturbation analysis.

## Notable Applications and Implementations

| Application | Mechanism | Domain |
|-------------|-----------|--------|
| **Spectral clustering** | Embed vertices using bottom eigenvectors of $\mathcal{L}$; cluster in embedding space | Machine learning, image segmentation |
| **Graph partitioning** | Fiedler vector bisection; normalized cuts | VLSI design, parallel computing |
| **Random walks** | $L_{\text{rw}} = I - P$; eigenvalues govern mixing time | Network science, Markov chains |
| **Diffusion / heat equation** | $\frac{\partial \mathbf{f}}{\partial t} = -L \mathbf{f}$; solution $\mathbf{f}(t) = e^{-tL} \mathbf{f}(0)$ | Physics, information spreading |
| **DeGroot learning** | Consensus dynamics $\mathbf{x}(t+1) = P \mathbf{x}(t)$ where $P = I - D^{-1}L$ | Social learning, opinion dynamics |
| **Graph signal processing** | Graph Fourier transform via eigenvectors of $L$; filtering in spectral domain | Sensor networks, brain imaging |
| **Effective resistance** | $R_{ij} = (e_i - e_j)^\top L^+ (e_i - e_j)$ | Electrical networks, network robustness |
| **Graph neural networks** | Spectral convolution: $g_\theta \star x = U g_\theta(\Lambda) U^\top x$ where $U$ = eigenvectors of $L$ | Deep learning on graphs |
| **Dimensionality reduction** | Laplacian eigenmaps: embed using bottom eigenvectors of $L$ | Manifold learning |
| **Network synchronization** | Eigenvalues of $L$ determine synchronization thresholds | Coupled oscillators, power grids |

## Connection to Diffusion and Heat Equation

The graph Laplacian governs discrete diffusion processes in exact analogy to the continuous heat equation. The **graph heat equation** is:

$$\frac{\partial \mathbf{f}(t)}{\partial t} = -L \, \mathbf{f}(t)$$

with solution $\mathbf{f}(t) = e^{-tL} \mathbf{f}(0)$, where the **heat kernel** $H_t = e^{-tL} = U e^{-t\Lambda} U^\top$ uses the eigendecomposition $L = U \Lambda U^\top$. The eigenvalues $\lambda_i$ control the decay rate of each spectral component: high-frequency (large $\lambda_i$) components dissipate quickly, while the constant component ($\lambda_1 = 0$) persists forever.

This connects to **random walks**: the random walk normalized Laplacian $L_{\text{rw}} = I - P$ implies that $P = I - L_{\text{rw}}$. The random walk transition rule $\mathbf{p}(t+1) = P \mathbf{p}(t)$ is a discrete-time version of the heat equation. The mixing rate of the random walk is governed by the *spectral gap* $1 - \lambda_2(P) = \lambda_2(L_{\text{rw}})$: a larger spectral gap means faster convergence to the stationary distribution.

## Connection to Graph Signal Processing

In **graph signal processing** (GSP), the eigenvectors of the graph Laplacian serve as the **graph Fourier basis**, analogous to complex exponentials in classical Fourier analysis. The **graph Fourier transform** (GFT) of a signal $\mathbf{x} \in \mathbb{R}^n$ is:

$$\hat{\mathbf{x}} = U^\top \mathbf{x}$$

where $U$ is the matrix of eigenvectors of $L$ (or $\mathcal{L}$). The eigenvalues $\lambda_i$ play the role of *frequencies*: eigenvectors corresponding to small eigenvalues are "smooth" (low-frequency) signals that vary slowly across the graph, while those corresponding to large eigenvalues are "rough" (high-frequency) signals that oscillate rapidly.

This framework enables:
- **Spectral filtering**: $\mathbf{y} = U \, h(\Lambda) \, U^\top \mathbf{x}$ for filter function $h$
- **Low-pass filtering**: Retaining only low-frequency components for denoising
- **Band-pass filtering**: Isolating signals at specific graph frequencies
- **Wavelets on graphs**: Multi-scale analysis using spectral graph wavelets (Hammond, Vandergheynst, Gribonval, 2011)

## Challenges and Limitations

### Computational Challenges
- **Eigendecomposition cost**: Full eigendecomposition of an $n \times n$ Laplacian is $O(n^3)$, prohibitive for large graphs. Approximation methods (Lanczos iteration, randomized SVD) or polynomial filter approximations (Chebyshev polynomials) are needed.
- **Sparsity dependence**: While the Laplacian inherits the sparsity pattern of $A$, spectral methods on dense graphs remain expensive.
- **Pseudoinverse computation**: Computing $L^+$ for effective resistance or commute-time calculations requires careful numerical handling.

### Theoretical Limitations
- **Directed graphs**: The standard Laplacian loses symmetry for directed graphs; the theory is substantially less developed, and multiple competing definitions exist.
- **Hypergraphs**: Extension to hypergraphs (edges connecting more than two vertices) requires careful generalization; multiple non-equivalent definitions have been proposed.
- **Dynamic graphs**: The Laplacian is defined for a static snapshot; for time-varying graphs, one must recompute or track spectral perturbations.
- **Degree heterogeneity**: The combinatorial Laplacian's spectrum is dominated by high-degree vertices, which is why normalized variants are preferred for heterogeneous networks.

### Practical Limitations
- **Sensitivity to graph construction**: In applications where the graph must be constructed from data (e.g., k-nearest neighbor graphs for clustering), spectral results are sensitive to the choice of $k$, the similarity function, and noise in the data.
- **Resolution limit**: Spectral methods based on the Fiedler vector cannot detect communities smaller than $\sqrt{n}$ in some settings (analogous to the modularity resolution limit).
- **Interpretation of higher eigenvectors**: While $\lambda_2$ and its eigenvector have clear interpretations, the meaning of higher Laplacian eigenvalues and eigenvectors is less intuitive and problem-dependent.

## Related Terms

- **[Spectral Graph Theory](term_spectral_graph_theory.md)**: The mathematical field studying graph properties through eigenvalues and eigenvectors of associated matrices; the graph Laplacian is its central object
- **[Adjacency Matrix](term_adjacency_matrix.md)**: The binary (or weighted) matrix $A$ encoding graph connectivity; the Laplacian is $L = D - A$
- **[Algebraic Connectivity](term_algebraic_connectivity.md)**: The second-smallest Laplacian eigenvalue $\lambda_2$, introduced by Fiedler; measures how well-connected a graph is
- **[Spectral Clustering](term_spectral_clustering.md)**: Clustering method that embeds data using Laplacian eigenvectors, then applies k-means; the primary machine learning application of the graph Laplacian
- **[DeGroot Learning](term_degroot_learning.md)**: Opinion dynamics model $\mathbf{x}(t+1) = P\mathbf{x}(t)$ where $P = I - D^{-1}L$; convergence rate governed by Laplacian spectral gap
- **[Community Detection](term_community_detection.md)**: Graph partitioning into densely connected subgroups; spectral methods use Laplacian eigenvectors as an alternative to modularity optimization
- **[Modularity](term_modularity.md)**: The modularity matrix $B$ is analogous to the Laplacian (symmetric, zero row sums) but encodes community structure via deviation from the configuration model null; spectral modularity methods use eigenvectors of $B$ rather than $L$
- **[Graph](term_graph.md)**: The underlying discrete structure $G = (V, E)$ on which the Laplacian is defined
- **[Graph Neural Networks](term_gnn.md)**: Spectral GNN convolution is defined via the Laplacian eigendecomposition; ChebNet and GCN approximate Laplacian spectral filters

## References

### External Sources

- [Chung, F. R. K. (1997). *Spectral Graph Theory*. CBMS Regional Conference Series in Mathematics, No. 92. American Mathematical Society.](https://mathweb.ucsd.edu/~fan/research/revised.html) — Definitive monograph on the normalized Laplacian; covers Cheeger inequalities, heat kernels, and connections to differential geometry
- [Mohar, B. (1991). "The Laplacian Spectrum of Graphs." *Graph Theory, Combinatorics, and Applications*, Vol. 2, pp. 871-898.](https://users.fmf.uni-lj.si/mohar/Papers/Spec.pdf) — Comprehensive survey of combinatorial Laplacian eigenvalue properties and their graph-theoretic interpretations
- [Von Luxburg, U. (2007). "A Tutorial on Spectral Clustering." *Statistics and Computing*, 17(4), pp. 395-416.](https://people.csail.mit.edu/dsontag/courses/ml14/notes/Luxburg07_tutorial_spectral_clustering.pdf) — Accessible tutorial connecting graph Laplacian theory to spectral clustering algorithms; standard ML reference
- [Spielman, D. A. (2012). "Spectral Graph Theory." Chapter 16 in *Combinatorial Scientific Computing*.](http://www.cs.yale.edu/homes/spielman/PAPERS/SGTChapter.pdf) — Modern treatment covering Laplacian solvers, sparsification, and algorithmic applications
- [Shuman, D. I., Narang, S. K., Frossard, P., Ortega, A., & Vandergheynst, P. (2013). "The Emerging Field of Signal Processing on Graphs." *IEEE Signal Processing Magazine*, 30(3), pp. 83-98.](https://doi.org/10.1109/MSP.2012.2235192) — Foundational paper defining graph signal processing; graph Fourier transform via Laplacian eigenvectors
- [Kirchhoff, G. (1847). "Ueber die Auflosung der Gleichungen, auf welche man bei der Untersuchung der linearen Vertheilung galvanischer Strome gefuhrt wird." *Annalen der Physik*, 148(12), pp. 497-508.](https://doi.org/10.1002/andp.18471481202) — Original paper introducing the Kirchhoff matrix and the Matrix-Tree Theorem
- [Fiedler, M. (1973). "Algebraic Connectivity of Graphs." *Czechoslovak Mathematical Journal*, 23(2), pp. 298-305.](https://dml.cz/handle/10338.dmlcz/101168) — Introduced algebraic connectivity ($\lambda_2$) and the Fiedler vector
- [Wikipedia: Laplacian Matrix](https://en.wikipedia.org/wiki/Laplacian_matrix) — Overview of definitions, properties, and variants
