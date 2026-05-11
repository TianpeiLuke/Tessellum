---
tags:
  - resource
  - terminology
  - signal_processing
  - spectral_graph_theory
  - network_science
  - graph_theory
  - graph_neural_networks
keywords:
  - graph signal processing
  - GSP
  - graph Fourier transform
  - GFT
  - graph spectral domain
  - vertex domain
  - spectral filtering
  - graph wavelets
  - graph convolution
  - vertex-frequency analysis
  - sampling on graphs
  - bandlimited graph signals
topics:
  - Signal Processing
  - Spectral Graph Theory
  - Network Science
  - Graph Neural Networks
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Graph Signal Processing (GSP)

## Definition

**Graph signal processing** (GSP) is the extension of classical signal processing concepts -- filtering, Fourier analysis, sampling, interpolation, and wavelet transforms -- to signals defined on the vertices of weighted graphs. In classical signal processing, signals live on regular domains (time series on the integer lattice, images on a 2D grid), and the discrete Fourier transform provides the frequency decomposition. In GSP, the underlying domain is an arbitrary weighted graph $G = (V, E, W)$, and a **graph signal** is a function $f: V \to \mathbb{R}$ that assigns a scalar value to each vertex, equivalently represented as a vector $\mathbf{x} \in \mathbb{R}^n$ where $n = |V|$.

The key insight of GSP is that the eigenvectors of the **graph Laplacian** $L = D - W$ (or its normalized variant $\mathcal{L} = D^{-1/2} L D^{-1/2}$) serve as the frequency basis for graph signals, analogous to complex exponentials in classical Fourier analysis. This enables the definition of a **graph Fourier transform** (GFT), spectral filtering, and frequency-domain analysis on irregular, non-Euclidean domains. The framework provides principled tools for analyzing data supported on networks -- sensor measurements distributed across a geographic region, brain activity signals on a cortical connectivity graph, or user attributes on a social network.

GSP unifies ideas from spectral graph theory, approximation theory, and harmonic analysis on discrete structures, and has become a foundational framework for understanding and designing graph neural networks.

## Historical Context

| Year | Milestone | Contributor(s) |
|------|-----------|-----------------|
| 1997 | Normalized Laplacian as spectral operator for graphs | Fan Chung |
| 2003 | Diffusion wavelets on graphs and manifolds | Coifman and Maggioni |
| 2011 | Spectral graph wavelet transform (SGWT) | Hammond, Vandergheynst, Gribonval |
| 2013 | "The Emerging Field of Signal Processing on Graphs" | Shuman, Narang, Frossard, Ortega, Vandergheynst |
| 2013 | Discrete signal processing on graphs (algebraic framework) | Sandryhaila and Moura |
| 2014 | Graph frequency analysis and directed graph extensions | Sandryhaila and Moura |
| 2015 | Sampling theory for bandlimited graph signals | Anis, Gadde, Ortega |
| 2016 | ChebNet: Chebyshev polynomial spectral filters for GNNs | Defferrard, Bresson, Vandergheynst |
| 2017 | GCN: first-order spectral approximation for semi-supervised learning | Kipf and Welling |
| 2018 | Comprehensive GSP survey in *Proceedings of the IEEE* | Ortega, Frossard, Kovacevic, Moura, Vandergheynst |
| 2023 | "GSP: History, Development, Impact, and Outlook" | Leus, Marques, Moura, Ortega, Shuman |

Graph signal processing emerged as a coherent field around 2013 from two complementary perspectives. **Shuman et al. (2013)** formalized the Laplacian-eigenvector approach, defining the graph Fourier transform, spectral filtering, and multi-scale analysis by analogy with continuous signal processing. Independently, **Sandryhaila and Moura (2013, 2014)** developed an algebraic signal processing framework using the adjacency matrix (or any "graph shift operator") as the foundational object, enabling analysis on directed graphs. These two schools -- Laplacian-based (spectral) and adjacency-based (algebraic) -- have since converged into a unified framework.

The field built on earlier work in spectral graph theory (Chung 1997), diffusion on graphs (Coifman and Maggioni 2003), and the spectral graph wavelet transform (Hammond et al. 2011). The 2018 survey by Ortega et al. consolidated the theoretical foundations and applications, establishing GSP as a mature subfield within signal processing.

## Taxonomy

### Core Domains of Analysis

| Domain | Representation | Operations | Analogy to Classical SP |
|--------|---------------|------------|------------------------|
| **Vertex domain** | Signal $\mathbf{x} \in \mathbb{R}^n$ on graph vertices | Localization, shifting, windowing | Time/spatial domain |
| **Graph spectral domain** | Coefficients $\hat{\mathbf{x}} = U^\top \mathbf{x}$ | Filtering, frequency selection | Frequency domain |
| **Vertex-frequency domain** | Joint localization in vertex and frequency | Windowed graph Fourier transform, graph wavelets | Time-frequency domain |

### Graph Shift Operators

| Operator | Definition | Proponents | Advantages |
|----------|-----------|------------|------------|
| **Combinatorial Laplacian** $L = D - W$ | Shuman et al. (2013) | GSP spectral school | Positive semidefinite; eigenvalues = frequencies; smoothness via $\mathbf{x}^\top L \mathbf{x}$ |
| **Normalized Laplacian** $\mathcal{L} = D^{-1/2} L D^{-1/2}$ | Shuman et al. (2013) | GSP spectral school | Bounded spectrum $[0, 2]$; degree-invariant |
| **Adjacency matrix** $A$ | Sandryhaila and Moura (2013) | Algebraic SP school | Works for directed graphs; shift = signal diffusion along edges |
| **Random walk matrix** $P = D^{-1}A$ | Various | Diffusion approach | Direct probabilistic interpretation; connection to PageRank |

### Spectral Filter Approximation Methods

| Method | Filter Form | Complexity | Locality |
|--------|-------------|------------|----------|
| **Exact spectral** | $h(\Lambda) = \text{diag}(h(\lambda_1), \ldots, h(\lambda_n))$ | $O(n^2)$ after eigendecomposition | Global |
| **Chebyshev polynomial** | $h(L) \approx \sum_{k=0}^{K} \theta_k T_k(\tilde{L})$ | $O(K \cdot |E|)$ | $K$-hop local |
| **ARMA filter** | Rational function of $L$ | $O(K \cdot |E|)$ per iteration | Approximately local |
| **Cayley filter** | Complex rational using Cayley transform | $O(K \cdot |E|)$ | Narrow band-pass |
| **Lanczos approximation** | Krylov subspace projection | $O(K \cdot |E|)$ | Adaptive |

## Key Properties

- **Graph Fourier Transform (GFT)**: Given the eigendecomposition $L = U \Lambda U^\top$ where $U = [u_1 | u_2 | \cdots | u_n]$ are eigenvectors and $\Lambda = \text{diag}(\lambda_1, \ldots, \lambda_n)$ are eigenvalues, the GFT of a graph signal $\mathbf{x}$ is $\hat{\mathbf{x}} = U^\top \mathbf{x}$ and the inverse GFT is $\mathbf{x} = U \hat{\mathbf{x}}$.

- **Graph frequencies as eigenvalues**: The Laplacian eigenvalues $0 = \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$ serve as graph frequencies. Small eigenvalues correspond to low frequencies (smooth signals), large eigenvalues to high frequencies (oscillatory signals). This is justified by the Rayleigh quotient: $\lambda_k = \frac{u_k^\top L u_k}{u_k^\top u_k} = \frac{\sum_{(i,j) \in E} w_{ij}(u_k(i) - u_k(j))^2}{\|u_k\|^2}$, which measures signal variation across edges.

- **Spectral filtering**: A graph spectral filter with frequency response $h(\cdot)$ applied to signal $\mathbf{x}$ produces $\mathbf{y} = h(L) \mathbf{x} = U \, h(\Lambda) \, U^\top \mathbf{x}$, where $h(\Lambda) = \text{diag}(h(\lambda_1), \ldots, h(\lambda_n))$. This generalizes classical convolution: multiplication in the spectral domain equals filtering in the vertex domain.

- **Low-frequency signals are smooth**: A low-pass filtered graph signal varies slowly across connected vertices -- neighboring nodes (connected by high-weight edges) have similar values. This corresponds to small Dirichlet energy $\mathbf{x}^\top L \mathbf{x} = \sum_{(i,j) \in E} w_{ij}(x_i - x_j)^2$.

- **High-frequency signals oscillate**: A high-pass filtered graph signal exhibits rapid variation between adjacent vertices, analogous to high-frequency oscillation in classical signals.

- **Bandlimited graph signals**: A graph signal is **$\omega$-bandlimited** (or **$K$-bandlimited**) if its GFT coefficients are zero for frequencies above a cutoff: $\hat{x}(\lambda_k) = 0$ for $\lambda_k > \omega$. This enables sampling theory on graphs.

- **Graph convolution**: The convolution of two graph signals $\mathbf{x}$ and $\mathbf{y}$ is defined in the spectral domain as pointwise multiplication: $\mathbf{x} \ast_G \mathbf{y} = U ((U^\top \mathbf{x}) \odot (U^\top \mathbf{y}))$, directly generalizing the convolution theorem.

- **Parseval's identity on graphs**: $\|\mathbf{x}\|^2 = \|\hat{\mathbf{x}}\|^2$, since $U$ is orthogonal. Energy is preserved between vertex and spectral domains.

- **Total variation on graphs**: The graph total variation $\text{TV}(\mathbf{x}) = \sum_{(i,j) \in E} w_{ij} |x_i - x_j|$ provides an $\ell_1$ measure of signal smoothness, used in regularization and denoising.

- **Uncertainty principle on graphs**: There exists a fundamental trade-off between localization in the vertex domain and localization in the graph spectral domain, analogous to the Heisenberg uncertainty principle. A graph signal cannot be simultaneously concentrated on a few vertices and a few graph frequencies.

## Notable Systems / Implementations

| System / Algorithm | Mechanism | Application |
|-------------------|-----------|-------------|
| **Graph wavelets (Hammond et al., 2011)** | Spectral graph wavelet transform using scaled generating kernel $g(t\lambda)$ applied in Laplacian eigenbasis | Multi-scale analysis on graphs; brain imaging |
| **ChebNet (Defferrard et al., 2016)** | $K$-order Chebyshev polynomial approximation of spectral filters: $h(L) \approx \sum_{k=0}^{K} \theta_k T_k(\tilde{L})$ | Graph classification; avoids eigendecomposition |
| **GCN (Kipf and Welling, 2017)** | First-order Chebyshev approximation: $H' = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H \Theta)$ with renormalization trick | Semi-supervised node classification |
| **PyGSP** | Python library implementing GFT, spectral filtering, graph wavelets, and visualization | Research and prototyping for GSP |
| **GSPBox (EPFL)** | MATLAB toolbox for graph signal processing | Academic research |
| **Sampling on graphs (Anis et al., 2016)** | Optimal sampling set selection for bandlimited graph signals using spectral proxies | Signal reconstruction from partial observations |
| **ARMA filters on graphs** | Auto-regressive moving average rational filters in spectral domain | Flexible frequency response design |
| **Graph scattering transform** | Cascaded wavelet modulus operations on graphs (Gama et al., 2019) | Stability to graph perturbations |

## Applications

| Domain | Application | GSP Technique |
|--------|------------|---------------|
| **Sensor networks** | Distributed estimation, denoising, anomaly detection | Graph filtering, sampling, reconstruction |
| **Brain imaging (fMRI/EEG)** | Functional connectivity analysis, brain signal denoising | Graph wavelets on cortical meshes; spectral decomposition of brain signals |
| **Social network analysis** | Opinion dynamics modeling, influence propagation analysis | Graph spectral analysis of user attribute signals |
| **Point cloud processing** | 3D shape analysis, surface denoising, compression | Graph Fourier transform on k-NN graphs of point clouds |
| **Recommender systems** | Collaborative filtering on user-item bipartite graphs | Low-pass graph filtering of rating signals |
| **Image and video processing** | Non-local denoising, inpainting, compression | Graph-based transform coding; adaptive graph construction |
| **Transportation networks** | Traffic flow prediction, congestion analysis | Spatio-temporal graph signal analysis |
| **Power grid monitoring** | State estimation, fault detection | Smooth signal assumption on grid topology |
| **Genomics and proteomics** | Gene expression analysis on gene regulatory networks | Graph spectral analysis of expression signals |

## Challenges and Limitations

### Computational Challenges
- **Eigendecomposition bottleneck**: Full eigendecomposition of the Laplacian is $O(n^3)$, prohibitive for graphs with millions of vertices. Polynomial filter approximations (Chebyshev, Lanczos) avoid this but introduce approximation error and limit filter design flexibility.
- **Graph construction sensitivity**: When the graph must be inferred from data (e.g., constructing similarity graphs from sensor positions), GSP results are sensitive to the choice of similarity function, sparsification threshold, and noise in the data.
- **Dynamic graphs**: The spectral basis changes when the graph topology evolves over time. Tracking spectral changes efficiently (online eigendecomposition, perturbation-based updates) remains an active area.

### Theoretical Challenges
- **Non-uniqueness of graph frequency**: The Laplacian-based and adjacency-based definitions of graph frequency do not always agree, especially for directed graphs. The choice of graph shift operator fundamentally affects the spectral interpretation.
- **No canonical ordering of frequencies**: Unlike classical frequencies which are naturally ordered by oscillation rate, graph frequencies (Laplacian eigenvalues) may have multiplicities and degenerate eigenspaces, complicating the definition of bandlimitedness.
- **Directed graph extensions**: The Laplacian of a directed graph is not symmetric, so eigenvectors are not orthogonal and may be complex-valued. Defining a consistent GFT for directed graphs remains an open problem with competing approaches (Jordan normal form, singular value decomposition, magnetic Laplacian).
- **Uncertainty principle tightness**: The graph uncertainty principle bounds are generally looser than their continuous counterparts, and tight characterizations exist only for specific graph families.

### Practical Challenges
- **Scalability of spectral methods**: While polynomial approximations enable scalable filtering, many GSP operations (optimal sampling, graph wavelet design) still require knowledge of the full spectrum or at least the spectral range.
- **Interpretability of graph frequencies**: The physical meaning of "frequency" on an arbitrary graph is less intuitive than temporal or spatial frequency. Domain experts may find graph spectral concepts difficult to interpret without careful visualization.
- **Joint time-vertex analysis**: For signals that evolve over time on a graph (e.g., traffic data), the joint time-vertex Fourier transform involves tensor products of temporal and graph spectral bases, increasing complexity substantially.

## Related Terms
- **[Graph Laplacian](term_graph_laplacian.md)**: The fundamental matrix operator in GSP; its eigendecomposition defines the graph Fourier basis and graph frequencies
- **[Spectral Graph Theory](term_spectral_graph_theory.md)**: The mathematical foundation underlying GSP; studies graph structure through eigenvalues and eigenvectors of associated matrices
- **[Adjacency Matrix](term_adjacency_matrix.md)**: Alternative graph shift operator used in the algebraic signal processing framework of Sandryhaila and Moura
- **[Algebraic Connectivity](term_algebraic_connectivity.md)**: The second-smallest Laplacian eigenvalue $\lambda_2$; in GSP, it represents the lowest non-trivial graph frequency
- **[Eigenvector Centrality](term_eigenvector_centrality.md)**: Centrality measure using the dominant eigenvector of the adjacency matrix; connects to spectral analysis of influence signals on networks
- **[Spectral Clustering](term_spectral_clustering.md)**: Clustering via Laplacian eigenvectors; can be interpreted as low-pass filtering of cluster indicator signals in the GSP framework
- **[Graph Neural Networks](term_gnn.md)**: Deep learning architectures on graphs; spectral GNNs (ChebNet, GCN) are directly derived from GSP spectral filtering theory
- **[Graph](term_graph.md)**: The underlying discrete structure $G = (V, E)$ on which graph signals are defined

## References

### Vault Sources

### External Sources
- [Shuman, D. I., Narang, S. K., Frossard, P., Ortega, A., and Vandergheynst, P. (2013). "The Emerging Field of Signal Processing on Graphs." *IEEE Signal Processing Magazine*, 30(3), 83-98.](https://doi.org/10.1109/MSP.2012.2235192) -- foundational paper establishing the GSP framework; defines GFT, spectral filtering, and multi-scale analysis
- [Sandryhaila, A. and Moura, J. M. F. (2013). "Discrete Signal Processing on Graphs." *IEEE Transactions on Signal Processing*, 61(7), 1644-1656.](https://doi.org/10.1109/TSP.2013.2238935) -- algebraic signal processing approach using adjacency matrix as shift operator
- [Sandryhaila, A. and Moura, J. M. F. (2014). "Discrete Signal Processing on Graphs: Frequency Analysis." *IEEE Transactions on Signal Processing*, 62(12), 3042-3054.](https://doi.org/10.1109/TSP.2014.2321121) -- extends algebraic framework to graph frequency analysis and directed graphs
- [Ortega, A., Frossard, P., Kovacevic, J., Moura, J. M. F., and Vandergheynst, P. (2018). "Graph Signal Processing: Overview, Challenges, and Applications." *Proceedings of the IEEE*, 106(5), 808-828.](https://doi.org/10.1109/JPROC.2018.2820126) -- comprehensive survey consolidating GSP theory and applications
- [Hammond, D. K., Vandergheynst, P., and Gribonval, R. (2011). "Wavelets on Graphs via Spectral Graph Theory." *Applied and Computational Harmonic Analysis*, 30(2), 129-150.](https://doi.org/10.1016/j.acha.2010.04.005) -- spectral graph wavelet transform; multi-scale analysis on graphs
- [Anis, A., Gadde, A., and Ortega, A. (2016). "Efficient Sampling Set Selection for Bandlimited Graph Signals." *IEEE Transactions on Signal Processing*, 64(14), 3737-3751.](https://doi.org/10.1109/TSP.2016.2546233) -- sampling theory for graph signals; optimal vertex selection for reconstruction
- [Kipf, T. N. and Welling, M. (2017). "Semi-Supervised Classification with Graph Convolutional Networks." *ICLR 2017*.](https://arxiv.org/abs/1609.02907) -- GCN as first-order Chebyshev approximation of spectral graph filters
- [Defferrard, M., Bresson, X., and Vandergheynst, P. (2016). "Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering." *NeurIPS 2016*.](https://arxiv.org/abs/1606.09375) -- ChebNet; Chebyshev polynomial approximation enabling scalable spectral graph convolution
- [Leus, G., Marques, A. G., Moura, J. M. F., Ortega, A., and Shuman, D. I. (2023). "Graph Signal Processing: History, Development, Impact, and Outlook." *IEEE Signal Processing Magazine*, 40(4), 28-43.](https://doi.org/10.1109/MSP.2023.3262906) -- retrospective survey covering GSP history, impact on data science and deep learning, and future directions
