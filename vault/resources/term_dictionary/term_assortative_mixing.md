---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - statistics
  - complexity_science
  - social_network_analysis
keywords:
  - assortative mixing
  - assortativity
  - assortativity coefficient
  - degree correlation
  - disassortativity
  - disassortative mixing
  - mixing matrix
  - Newman assortativity
  - degree-degree correlation
  - homophily
  - network resilience
topics:
  - Network Science
  - Graph Theory
  - Complex Systems
  - Network Structure
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Assortative Mixing

## Definition

**Assortative mixing** (or **assortativity**) is a pattern in networks where nodes tend to connect to other nodes that are similar to themselves with respect to some property. In the most commonly studied case -- **degree assortativity** -- high-degree nodes preferentially connect to other high-degree nodes, and low-degree nodes preferentially connect to other low-degree nodes. The opposite pattern, where high-degree nodes preferentially connect to low-degree nodes, is called **disassortative mixing** (or **disassortativity**).

More formally, a network exhibits assortative mixing by some node attribute if the Pearson correlation coefficient between the attribute values of connected node pairs is positive. For degree assortativity, this means measuring the correlation between the degrees $k_i$ and $k_j$ at either end of each edge $(i, j)$ in the network. If this correlation is positive, the network is assortative; if negative, disassortative; if near zero, the network shows no degree-degree correlation (as in a randomly wired network).

Assortative mixing can be defined with respect to any node property -- not just degree. When the property is a **scalar** quantity (degree, age, income), the Pearson correlation coefficient is used. When the property is a **categorical** variable (type, group membership, ethnicity), a normalized trace of the mixing matrix quantifies the assortativity. This generality makes assortative mixing a unifying concept that connects network topology to node attributes, bridging structural analysis with attribute-based analysis.

## Historical Context

| Year | Milestone | Contributors |
|------|-----------|-------------|
| 2002 | Introduced the concept of assortative mixing in networks; measured degree-degree correlations across a wide range of real-world networks; demonstrated that social networks are assortative while technological and biological networks are disassortative | **M.E.J. Newman** |
| 2003 | Formalized the **mixing matrix** framework and derived the **assortativity coefficient** $r$ for both categorical and scalar node properties; provided the complete mathematical apparatus for measuring assortative mixing | **M.E.J. Newman** |
| 2001-2002 | Introduced the concept of **degree correlations** in scale-free networks through the conditional probability $P(k' | k)$ (average degree of neighbors as a function of node degree); showed that many real networks display non-trivial degree correlations | **Romualdo Pastor-Satorras, Alessandro Vespignani, Alexei Vazquez** |
| 2004 | Studied how degree correlations (assortativity) affect percolation thresholds and epidemic spreading on networks | **Vazquez, Moreno** |
| 2010 | Extended assortativity measures to **directed networks**, defining four distinct degree-degree correlations (in-in, in-out, out-in, out-out) | **Foster, Foster, Grassberger, Paczuski** |
| 2018 | Proposed **multiscale mixing patterns** that generalize assortativity beyond nearest-neighbor correlations to capture mixing at different topological scales | **Peel, Delvenne, Lambiotte** |

Newman's 2002 paper "Assortative mixing in networks" (*Physical Review Letters*, 89, 208701) was the foundational contribution. He observed that the tendency for like to connect with like had been extensively studied in sociology (under the name [homophily](term_homophily.md)) but had not been systematically measured across different classes of networks. His key empirical finding -- that social networks are assortative by degree while technological and biological networks are disassortative -- became one of the most cited structural dichotomies in network science.

## Taxonomy

### By Property Type

| Mixing Type | Property | Measure | Example |
|-------------|----------|---------|---------|
| **Degree assortativity** | Node degree (scalar) | Pearson correlation $r$ of degrees at edge endpoints | Social networks where popular people know popular people |
| **Categorical assortativity** | Discrete type / group membership | Normalized mixing matrix trace $r = \frac{\text{Tr}(\mathbf{e}) - \|\mathbf{e}^2\|}{1 - \|\mathbf{e}^2\|}$ | Ethnic homophily in friendship networks |
| **Scalar attribute assortativity** | Continuous node attribute (e.g., age, wealth) | Pearson correlation of attribute values at edge endpoints | Age-assortative mixing in contact networks |
| **Weighted assortativity** | Degree or attribute, weighted by edge weight | Weighted Pearson correlation | Trade networks where volume-weighted trade preferentially links similar-GDP countries |

### By Mixing Direction

| Pattern | Coefficient | Description | Typical Network Types |
|---------|-------------|-------------|----------------------|
| **Assortative** ($r > 0$) | Positive correlation | Like connects to like; hubs connect to hubs | Social networks, collaboration networks |
| **Disassortative** ($r < 0$) | Negative correlation | Unlike connects to unlike; hubs connect to low-degree nodes | Biological networks, technological networks, food webs |
| **Neutral** ($r \approx 0$) | No correlation | Degree of neighbors is independent of node degree | Erdos-Renyi random graphs, configuration model (by construction) |

### Empirical Values Across Network Classes (Newman, 2002)

| Network Type | Example Networks | Typical $r$ | Pattern |
|-------------|------------------|-------------|---------|
| **Social** | Physics coauthorship, film actors, company directors | $+0.12$ to $+0.36$ | Assortative |
| **Technological** | Internet (AS-level), power grid, peer-to-peer | $-0.19$ to $-0.04$ | Disassortative |
| **Biological** | Protein interactions, neural networks, food webs | $-0.27$ to $-0.16$ | Disassortative |
| **Information** | World Wide Web, citation networks | $-0.07$ to $+0.15$ | Mixed |

## Key Properties

- **Assortativity coefficient range**: The coefficient $r$ is bounded by $-1 \leq r \leq 1$. A value of $r = 1$ indicates perfect assortativity (every node connects only to nodes of identical degree or type), $r = -1$ indicates perfect disassortativity, and $r = 0$ indicates no correlation (random mixing)
- **Pearson correlation interpretation**: For degree assortativity on undirected networks, $r$ is exactly the Pearson correlation coefficient computed over all edges, treating each edge as a data point with two values (the degrees of its two endpoints): $r = \frac{\sum_{(i,j)} k_i k_j / M - \left[\sum_{(i,j)} (k_i + k_j) / 2M\right]^2}{\sum_{(i,j)} (k_i^2 + k_j^2) / 2M - \left[\sum_{(i,j)} (k_i + k_j) / 2M\right]^2}$ where the sums run over all $M$ edges
- **Mixing matrix formalization**: Newman defines the mixing matrix $\mathbf{e}$ where $e_{ij}$ is the fraction of edges connecting nodes of type $i$ to nodes of type $j$. For undirected networks, $\mathbf{e}$ is symmetric. The row/column sums $a_i = \sum_j e_{ij}$ give the fraction of edges incident to type-$i$ nodes. If mixing is random, $e_{ij} = a_i a_j$, and any deviation from this product form indicates assortative or disassortative mixing
- **Excess degree distribution**: The coefficient is properly computed using the **excess degree distribution** $q_k$ (the degree distribution of a node reached by following a random edge), not the raw degree distribution $p_k$; $q_k = (k+1) p_{k+1} / \langle k \rangle$
- **Neighbor degree function**: An alternative characterization uses $k_{nn}(k)$, the average degree of neighbors of nodes with degree $k$. If $k_{nn}(k)$ is increasing, the network is assortative; if decreasing, disassortative. This function provides a more detailed picture than the scalar coefficient $r$
- **Effect on giant component**: Assortative networks [percolate](term_percolation_theory_networks.md) more easily than their neutral counterparts -- they have a lower percolation threshold and a larger giant component for the same average degree. This is because high-degree nodes reinforcing each other creates a robust interconnected core
- **Resilience to targeted attack**: Assortative networks are more robust to targeted removal of high-degree nodes because the core of interconnected hubs provides redundant connectivity. Disassortative networks, where hubs connect to many low-degree nodes in a star-like topology, are more vulnerable because removing a hub disconnects many peripheral nodes
- **Epidemic spreading**: Degree correlations modify epidemic thresholds and spreading dynamics. On disassortative networks, epidemics spread more efficiently from hubs to the periphery; on assortative networks, epidemics may be initially confined to the hub core before spreading outward
- **Relationship to community structure**: Assortative mixing by a categorical attribute naturally produces [community structure](term_community_detection.md) -- groups of nodes densely connected internally and sparsely connected externally. Degree assortativity can also promote a form of structural community formation where hub-rich and hub-poor regions emerge
- **Configuration model baseline**: The [configuration model](term_configuration_model.md) produces networks with a specified [degree distribution](term_degree_distribution.md) but neutral mixing ($r \approx 0$) by construction, making it the natural null model against which assortative or disassortative mixing is measured

## Notable Systems / Implementations

| System / Network | Assortativity Value | Pattern | Key Observation |
|-----------------|-------------------|---------|-----------------|
| **Physics coauthorship** | $r \approx +0.36$ | Strongly assortative | Prolific researchers coauthor with other prolific researchers |
| **Film actor collaboration** | $r \approx +0.21$ | Assortative | Stars act with other stars |
| **Company director boards** | $r \approx +0.28$ | Assortative | Well-connected directors share boards with other well-connected directors |
| **Internet (AS-level)** | $r \approx -0.19$ | Disassortative | Large ISPs connect to many small ISPs in a hub-spoke topology |
| **Protein interaction (yeast)** | $r \approx -0.16$ | Disassortative | Hub proteins bind to many specific low-degree partners |
| **C. elegans neural network** | $r \approx -0.23$ | Disassortative | Highly connected neurons link to many sparsely connected neurons |
| **Power grid** | $r \approx -0.003$ | Approximately neutral | Grid topology is near-planar with limited degree variation |
| **World Wide Web** | $r \approx -0.07$ | Weakly disassortative | Authoritative pages link to many content pages, but reciprocal linking among popular sites adds assortative tendency |

## Applications

| Domain | Application | Assortative Mixing Insight |
|--------|------------|---------------------------|
| **Epidemiology** | Disease transmission modeling on contact networks | Assortative mixing concentrates transmission within subpopulations of similar connectivity; vaccination strategies must account for whether the contact network is assortative (target hub clusters) or disassortative (target individual hubs) |
| **Network robustness** | Infrastructure design and protection | Assortative networks maintain connectivity under targeted hub attacks due to redundant hub-hub links; disassortative networks are more fragile to targeted attacks but robust to random failures |
| **Social media analysis** | Echo chamber detection and polarization measurement | Assortative mixing by political orientation or ideology quantifies the degree of partisan segregation in online networks |
| **Fraud detection** | Identifying coordinated abuse networks | Anomalous assortativity patterns -- e.g., clusters of accounts with suspiciously similar attributes or connectivity -- can signal coordinated manipulation or bot networks |
| **Ecology** | Food web structure analysis | Disassortative mixing in food webs (generalist predators consuming many specialist prey) shapes ecosystem stability and species coexistence |
| **Neuroscience** | Brain network architecture | Disassortative wiring in neural networks promotes efficient signal distribution from integration hubs to specialized processing regions |

## Challenges and Limitations

### Measurement Challenges
- **Finite-size bias**: In small networks, the assortativity coefficient $r$ can be biased, and its variance is large; confidence intervals should be computed via bootstrap or jackknife resampling
- **Degree range effects**: Networks with narrow degree distributions (e.g., near-regular lattices) produce assortativity coefficients near zero regardless of actual mixing patterns, because there is insufficient degree variation to correlate
- **Structural constraints**: The maximum and minimum achievable values of $r$ depend on the degree sequence itself -- not all degree sequences permit $r = +1$ or $r = -1$; Newman and others have developed normalized measures to account for this

### Conceptual Challenges
- **Scalar reduction**: The single coefficient $r$ compresses the full mixing matrix (or the function $k_{nn}(k)$) into one number, potentially masking rich structure such as non-monotonic degree correlations or scale-dependent mixing patterns
- **Multiscale mixing**: Peel, Delvenne, and Lambiotte (2018) showed that assortative mixing measured at nearest-neighbor distance can differ qualitatively from mixing at longer network distances, suggesting that the standard coefficient captures only local correlations
- **Directed networks**: In directed networks, there are four distinct degree-degree correlations (in-in, in-out, out-in, out-out), and a single assortativity coefficient is insufficient; Foster et al. (2010) proposed extended measures

### Relationship to Other Concepts
- **Homophily vs. degree assortativity**: [Homophily](term_homophily.md) (nodes connecting to similar nodes by attribute) and degree assortativity (nodes connecting to similar-degree nodes) are conceptually related but statistically distinct; a network can be assortative by degree but not by any categorical attribute, or vice versa
- **Confounding with community structure**: Networks with strong community structure can appear assortative even without intrinsic degree-degree correlations, because within-community edges connect nodes of similar degree by construction

## Related Terms

- **[Homophily](term_homophily.md)**: The tendency for nodes to connect to similar nodes by attribute; assortative mixing by degree is the structural analog of homophily applied to connectivity rather than node attributes
- **[Degree Distribution](term_degree_distribution.md)**: The marginal distribution of node degrees; assortative mixing describes the joint distribution (degree correlations) that the degree distribution alone cannot capture
- **[Network Centrality](term_network_centrality.md)**: Centrality measures (degree, betweenness, closeness) quantify individual node importance; assortativity describes how centrality values are correlated across connected node pairs
- **[Community Detection](term_community_detection.md)**: Assortative mixing by categorical attributes directly produces community structure; degree assortativity also affects community detection algorithm performance
- **[Small-World Network](term_small_world_network.md)**: Small-world networks can exhibit varying assortativity; the interplay between clustering, short path lengths, and degree correlations shapes network function
- **[Random Graph](term_random_graph.md)**: Random graphs (Erdos-Renyi) have neutral degree mixing ($r \approx 0$) and serve as the null model against which assortativity is measured
- **[Configuration Model](term_configuration_model.md)**: Generates random graphs with a prescribed degree distribution but neutral mixing by construction; used to test whether observed assortativity exceeds random expectation
- **[Power Law](term_power_law.md)**: Scale-free networks with power-law degree distributions are typically disassortative; the interplay between fat-tailed degrees and mixing patterns has important consequences for resilience and spreading
- **[Preferential Attachment](term_preferential_attachment.md)**: The Barabasi-Albert growth mechanism produces weakly disassortative networks because new low-degree nodes preferentially attach to existing hubs
- **[Erdos-Renyi Model](term_erdos_renyi_model.md)**: The classical random graph model with Poisson degree distribution and no degree correlations; assortativity is approximately zero by construction

## References

### Vault Sources

### External Sources
- [Newman, M.E.J. (2002). "Assortative Mixing in Networks." *Physical Review Letters*, 89(20), 208701.](https://arxiv.org/abs/cond-mat/0205405) -- The foundational paper introducing the concept and measuring assortativity across social, technological, and biological networks
- [Newman, M.E.J. (2003). "Mixing Patterns in Networks." *Physical Review E*, 67(2), 026126.](https://arxiv.org/abs/cond-mat/0209450) -- The full mathematical treatment: mixing matrix formalization, assortativity coefficient derivation for both categorical and scalar properties, and empirical analysis
- [Newman, M.E.J. (2003). "The Structure and Function of Complex Networks." *SIAM Review*, 45(2), 167-256.](https://doi.org/10.1137/S003614450342480) -- Comprehensive review covering assortativity in the broader context of network science
- [Pastor-Satorras, R., Vazquez, A., & Vespignani, A. (2001). "Dynamical and Correlation Properties of the Internet." *Physical Review Letters*, 87(25), 258701.](https://arxiv.org/abs/cond-mat/0105161) -- Early study of degree-degree correlations in technological networks
- [Foster, J.G., Foster, D.V., Grassberger, P., & Paczuski, M. (2010). "Edge Direction and the Structure of Networks." *PNAS*, 107(24), 10815-10820.](https://doi.org/10.1073/pnas.0912671107) -- Extended assortativity measures to directed networks with four-fold degree correlations
- [Peel, L., Delvenne, J.-C., & Lambiotte, R. (2018). "Multiscale Mixing Patterns in Networks." *PNAS*, 115(16), 4057-4062.](https://www.pnas.org/doi/10.1073/pnas.1713019115) -- Generalized assortativity beyond nearest neighbors to multiscale mixing
- [Noldus, R. & Van Mieghem, P. (2015). "Assortativity in Complex Networks." *Journal of Complex Networks*, 3(4), 507-542.](https://doi.org/10.1093/comnet/cnv005) -- Comprehensive survey of assortativity measures, variants, and applications
- [Ben Davies. "Assortative Mixing." Blog post.](https://bldavies.com/blog/assortative-mixing/) -- Accessible mathematical exposition of the mixing matrix and assortativity coefficient
- [NetworkX: Assortativity Coefficients and Correlation Measures](https://networkx.org/nx-guides/content/algorithms/assortativity/correlation.html) -- Practical computational implementation and examples
