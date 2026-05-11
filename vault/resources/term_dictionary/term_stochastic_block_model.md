---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - random_graph_theory
  - community_detection
  - statistical_inference
keywords:
  - stochastic block model
  - SBM
  - planted partition model
  - block model
  - degree-corrected SBM
  - DC-SBM
  - community structure
  - generative network model
  - inter-group edge probability
  - intra-group edge probability
  - detectability threshold
topics:
  - Random Graph Theory
  - Network Science
  - Community Detection
  - Statistical Inference
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Stochastic Block Model (SBM)

## Definition

The **Stochastic Block Model (SBM)** is a generative model for random graphs that incorporates latent community structure. Given $n$ nodes partitioned into $K$ groups (blocks), the probability that an edge exists between nodes $i$ and $j$ depends solely on their group memberships $z_i$ and $z_j$:

$$P(A_{ij} = 1 \mid z_i, z_j) = \theta_{z_i, z_j}$$

where $\theta$ is a $K \times K$ symmetric matrix of edge probabilities and $A$ is the adjacency matrix. The full likelihood factors as:

$$L(A \mid \theta, z) = \prod_{i < j} \theta_{z_i, z_j}^{A_{ij}} (1 - \theta_{z_i, z_j})^{1 - A_{ij}}$$

This formulation assumes conditional independence: given community assignments, edge presence between any pair of nodes is independent. The SBM provides the canonical generative model that community detection algorithms attempt to recover -- it defines what "community structure" means in a probabilistically precise sense.

When $K = 1$, the SBM reduces to the Erdos-Renyi $G(n, p)$ model. When $K > 1$ and intra-group probabilities exceed inter-group probabilities ($\theta_{kk} > \theta_{kl}$ for $k \neq l$), the model generates **[assortative](term_assortative_mixing.md)** (homophilic) networks. The reverse produces **disassortative** mixing patterns.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1983 | **Holland, Laskey, Leinhardt** | Introduced the stochastic blockmodel in "Stochastic Blockmodels: First Steps" (*Social Networks*, 5(2), 109-137), generalizing deterministic blockmodels from social network analysis |
| 2001 | **Condon, Karp** | Formalized the **planted partition model** (symmetric SBM with equal-sized groups) and analyzed polynomial-time recovery algorithms |
| 2008 | **Jackson** | Presented the SBM in *Social and Economic Networks* (Ch. 3) as one of the canonical random graph models for social network formation, alongside Erdos-Renyi and configuration models |
| 2011 | **Decelle, Krzakala, Moore, Zdeborova** | Established the information-theoretic **detectability threshold** for the symmetric SBM using methods from statistical physics; below this threshold, no algorithm can recover community structure better than chance |
| 2011 | **Karrer, Newman** | Proposed the **degree-corrected SBM (DC-SBM)**, allowing heterogeneous degree distributions within blocks; dramatically improved fit to real-world networks |
| 2014 | **Mossel, Neeman, Sly** | Proved that the Decelle et al. conjecture is correct for the 2-block symmetric case, establishing the exact computational threshold |
| 2017 | **Abbe** | Published a comprehensive survey ("Community Detection and Stochastic Block Models") unifying recovery, detection, and estimation results |

## Taxonomy

| Variant | Modification | Key Feature |
|---------|-------------|-------------|
| **Standard SBM** | $K$ blocks with $K \times K$ probability matrix $\theta$ | Simplest form; all nodes in a block are stochastically equivalent |
| **Planted partition model** | Symmetric SBM: $\theta_{kk} = p$, $\theta_{kl} = q$ for $k \neq l$, equal-sized groups | Simplest non-trivial case; primary model for theoretical analysis of community detection |
| **Degree-corrected SBM** | Each node $i$ has a degree parameter $\phi_i$; $P(A_{ij} = 1) = \phi_i \phi_j \theta_{z_i, z_j}$ | Accommodates hubs and heterogeneous degree distributions within blocks; extends the configuration model by adding group structure |
| **Mixed-membership SBM** | Each node has a distribution over group memberships rather than a single assignment | Allows nodes to participate in multiple communities; introduced by Airoldi et al. (2008) |
| **Hierarchical SBM** | Nested block structure with blocks organized in a tree | Captures multi-scale community structure; model selection determines depth automatically |

## Key Properties

- **Conditional independence**: Given community assignments, edges are independent Bernoulli random variables; this is the model's core structural assumption
- **Stochastic equivalence**: Nodes within the same block are statistically interchangeable -- they share identical connection probabilities to all other nodes
- **Identifiability**: The SBM is identifiable up to label permutation of the blocks; the number of free parameters grows as $K(K+1)/2$ (entries of $\theta$) plus $K - 1$ (group proportions)
- **Detectability threshold (Decelle et al. 2011)**: In the symmetric 2-block SBM with $n$ nodes, intra-block probability $a/n$, and inter-block probability $b/n$, community detection is information-theoretically impossible when $(a - b)^2 < 2(a + b)$; above this threshold, polynomial-time algorithms (e.g., belief propagation) succeed
- **Exact recovery vs. detection**: Two distinct regimes exist -- **detection** (better-than-random labeling) requires weaker signal than **exact recovery** (correctly labeling all $n$ nodes with high probability); the exact recovery threshold scales as $(\sqrt{a} - \sqrt{b})^2 > 2$ (Abbe and Sandon 2015)
- **Relationship to Erdos-Renyi**: With $K = 1$, the SBM reduces to $G(n, p)$; the SBM can thus be viewed as a minimal extension of the Erdos-Renyi model that introduces community structure
- **Relationship to configuration model**: The standard SBM constrains expected degree to be uniform within blocks; the degree-corrected SBM generalizes the configuration model by preserving degree sequences while adding group structure
- **ERGM connection**: The SBM can be expressed as a special case of exponential random graph models where the sufficient statistics are edge counts between and within blocks

## Applications

| Domain | Application | SBM Role |
|--------|------------|----------|
| **Social network analysis** | Identifying social groups, roles, and hierarchies | Generative model for role-based structure; recovers groups with similar relational patterns |
| **Neuroscience** | Mapping functional brain regions from connectivity data | Blocks correspond to functionally coupled brain areas |
| **Ecology** | Characterizing food web structure and trophic levels | Disassortative SBM captures predator-prey interactions across trophic levels |
| **Bibliometrics** | Detecting research communities from citation networks | Blocks identify disciplinary clusters |
| **Telecommunications** | Identifying communities in communication networks | Blocks reveal organizational or geographic structure |
| **Fraud detection** | Identifying coordinated account clusters | SBM-based methods detect unusually dense subgraphs indicative of collusion |

## Challenges and Limitations

- **Model selection (choosing $K$)**: The number of blocks must be estimated; approaches include integrated classification likelihood (ICL), Bayesian information criterion, and cross-validation, but none are universally reliable
- **Stochastic equivalence assumption**: Standard SBM assumes all nodes in a block have identical connection probabilities, which fails for networks with heterogeneous degree distributions (hubs); the degree-corrected SBM addresses this but adds parameters
- **Sparse regime difficulties**: In the regime where average degree is $O(1)$ (constant), community detection becomes fundamentally harder; below the Decelle et al. threshold, no algorithm can detect communities
- **Computational complexity**: Maximum likelihood estimation of the SBM is NP-hard in general; practical algorithms (spectral methods, belief propagation, variational EM) provide approximate solutions with different tradeoffs
- **Scalability**: Fitting SBMs to networks with millions of nodes requires specialized algorithms; naive approaches scale as $O(n^2)$ due to the need to consider all node pairs
- **Misspecification**: Real networks rarely follow an SBM exactly; model misspecification can lead to spurious community assignments, particularly when degree heterogeneity or overlapping memberships are present

## Related Terms

- **[Community Detection](term_community_detection.md)**: SBM is the canonical generative model that community detection algorithms attempt to recover; [modularity](term_modularity.md) maximization, spectral clustering, and belief propagation are all algorithms for inference under SBM-like assumptions
- **[Modularity](term_modularity.md)**: Newman (2016) proved that modularity maximization is equivalent to maximum-likelihood inference of a degree-corrected SBM with a specific parametric form
- **[Random Graph (Erdos-Renyi)](term_random_graph.md)**: SBM with $K = 1$ reduces to the Erdos-Renyi $G(n, p)$ model; the SBM is the minimal extension of ER that introduces community structure
- **[Configuration Model](term_configuration_model.md)**: The degree-corrected SBM extends the configuration model by adding block structure on top of a prescribed degree sequence; where CM ignores group structure, SBM adds it
- **[Exponential Random Graph Model (ERGM)](term_ergm.md)**: SBM can be expressed as a special case of ERGM where sufficient statistics are block-level edge counts; ERGMs are more flexible but harder to fit
- **[Homophily](term_homophily.md)**: The assortative SBM (higher intra-block than inter-block edge probability) provides a formal generative mechanism for homophily in networks
- **[Degree Distribution](term_degree_distribution.md)**: Standard SBM produces approximately Poisson degree distributions within blocks; the degree-corrected SBM was developed to preserve arbitrary degree sequences

## References

### Vault Sources

### External Sources
- [Holland, P.W., Laskey, K.B. & Leinhardt, S. (1983). "Stochastic Blockmodels: First Steps." *Social Networks*, 5(2), 109-137](https://doi.org/10.1016/0378-8733(83)90021-7) -- the foundational paper introducing the stochastic blockmodel
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Chapter 3](https://doi.org/10.2307/j.ctvcm4gh1) -- presents the SBM alongside other canonical random graph models for social network analysis
- [Karrer, B. & Newman, M.E.J. (2011). "Stochastic Blockmodels with a Growing Number of Classes." *Physical Review E*, 83, 016107](https://doi.org/10.1103/PhysRevE.83.016107) -- introduced the degree-corrected stochastic block model
- [Decelle, A., Krzakala, F., Moore, C. & Zdeborova, L. (2011). "Asymptotic Analysis of the Stochastic Block Model for Modular Networks and its Algorithmic Applications." *Physical Review E*, 84, 066106](https://doi.org/10.1103/PhysRevE.84.066106) -- established the information-theoretic detectability threshold
- [Abbe, E. (2017). "Community Detection and Stochastic Block Models: Recent Developments." *Journal of Machine Learning Research*, 18(177), 1-86](https://jmlr.org/papers/v18/16-480.html) -- comprehensive survey unifying detection, recovery, and estimation results
- [Airoldi, E.M., Blei, D.M., Fienberg, S.E. & Xing, E.P. (2008). "Mixed Membership Stochastic Blockmodels." *Journal of Machine Learning Research*, 9, 1981-2014](https://jmlr.org/papers/v9/airoldi08a.html) -- introduced the mixed-membership extension
- [Lee, A.B. & Funke, T. (2019). "A Review of Stochastic Block Models and Extensions for Graph Clustering." *Applied Network Science*, 4, 122](https://doi.org/10.1007/s41109-019-0232-2) -- review of SBM variants and graph clustering applications
