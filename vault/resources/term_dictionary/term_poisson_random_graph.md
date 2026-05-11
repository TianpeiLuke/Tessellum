---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - probability_theory
  - statistical_physics
keywords:
  - Poisson random graph
  - Poisson degree distribution
  - sparse random graph
  - null model
  - mean-field approximation
  - network null model
  - G(n,p) sparse regime
  - branching process
  - expected degree
  - Erdos-Renyi sparse
topics:
  - Random Graph Theory
  - Network Science
  - Statistical Mechanics of Networks
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Poisson Random Graph

## Definition

A **Poisson random graph** is the [Erdos-Renyi](term_erdos_renyi_model.md) $G(n,p)$ model in the **sparse regime** where $p = c/(n-1)$ for a fixed constant $c$. In this regime, each vertex has expected degree $c$, and the degree distribution converges to a **Poisson distribution** with mean $c$:

$$P(k) = \frac{c^k e^{-c}}{k!}$$

The Poisson random graph is the version of the ER model most used in network science, because real networks are sparse (average degree is finite and does not grow with network size). It serves as the **canonical null model** — the maximally random network consistent with a given average degree. Any structural property observed in a real network that deviates significantly from the Poisson random graph prediction is evidence of a meaningful, non-random organizing principle.

The name "Poisson random graph" emphasizes what distinguishes this model from real networks: its **thin-tailed, homogeneous degree distribution**. Real social and technological networks have [fat-tailed (power-law)](term_power_law.md) degree distributions with high-degree hubs that the Poisson distribution assigns essentially zero probability. This discrepancy is the single most important empirical fact motivating modern network science.

## Key Properties

- **Poisson degree distribution**: Degrees follow $\text{Poisson}(c)$ — the variance equals the mean, and the probability of very high degree decays exponentially. There are no hubs; the maximum degree scales as $O(\log n / \log \log n)$
- **[Giant component](term_giant_component.md) threshold at $c = 1$**: For $c < 1$ (subcritical), all components are trees of size $O(\log n)$; for $c > 1$ (supercritical), a unique giant component emerges containing fraction $s$ of vertices where $s = 1 - e^{-cs}$
- **Subcritical regime ($c < 1$)**: The graph is a forest with high probability; the expected component size containing a random vertex is $1/(1-c)$
- **Logarithmic path lengths**: Average shortest path $\sim \log n / \log c$, giving the "small-world" property — any two vertices in the giant component are reachable in $O(\log n)$ steps
- **Vanishing [clustering coefficient](term_clustering_coefficient.md)**: $C = c/(n-1) \to 0$ as $n \to \infty$ — real networks have clustering coefficients that remain positive and often exceed 0.1
- **Locally tree-like structure**: The neighborhood of a typical vertex has no short cycles with high probability; this enables the branching process approximation and mean-field analyses
- **Mean-field property**: Because the graph is locally tree-like and degree-homogeneous, many dynamical processes ([SIR](term_sir_model.md), [SIS](term_sis_model.md), [DeGroot learning](term_degroot_learning.md)) can be analyzed exactly using mean-field ODEs
- **Generating function framework**: The component size distribution and many other properties can be computed exactly via probability generating functions $G_0(x) = e^{c(x-1)}$ and the self-consistency equation $G_1(x) = e^{c(x-1)}$

## Role as Null Model

The Poisson random graph serves three distinct null-model functions in network science:

| Function | What It Tests | Example |
|----------|--------------|---------|
| **Degree-agnostic null** | Is the property explained by average degree alone? | Clustering: real networks have $C \gg c/n$, so clustering is NOT explained by density alone |
| **[Modularity](term_modularity.md) baseline** | Is the community structure real or artifact of random fluctuations? | Newman's [modularity](term_modularity.md) $Q$ compares edge density within groups to the Poisson random graph expectation |
| **Epidemic baseline** | Does network structure change epidemic behavior vs. well-mixed assumption? | SIS threshold on ER = $1/c$; on scale-free networks, threshold $\to 0$ — structure matters |

For testing whether properties are explained by the degree distribution (not just density), the [configuration model](term_configuration_model.md) is the appropriate null model instead.

## Comparison with Real Networks

| Property | Poisson Random Graph | Real Social Networks |
|----------|---------------------|---------------------|
| Degree distribution | Poisson (thin-tailed, $\sigma^2 = \mu$) | Power law / fat-tailed ($\sigma^2 \gg \mu$) |
| Maximum degree | $O(\log n / \log \log n)$ | $O(n^{1/(\alpha-1)})$ for power law with exponent $\alpha$ |
| Clustering coefficient | $c/(n-1) \to 0$ | $0.1 - 0.6$ (remains finite) |
| Community structure | None (homogeneous) | Strong modular organization |
| Degree correlations | None (independent edges) | [Assortative](term_assortative_mixing.md) (social) or disassortative (technological) |
| Path length | $O(\log n)$ | $O(\log n)$ (similar — both are "small worlds") |

The only property the Poisson random graph shares with real networks is short path lengths. Every other structural feature differs qualitatively — this is why network science exists as a field.

## Challenges and Limitations

- **Unrealistic degree distribution**: The thin Poisson tail assigns negligible probability to hubs that dominate real network dynamics (super-spreaders, influencers, critical infrastructure)
- **No clustering mechanism**: The model has no triadic closure — the probability that two neighbors of a node are connected equals the baseline $p$, not the elevated probability observed in social networks
- **Overly permissive as a null**: Because the Poisson random graph lacks so many real network features, almost any structural property appears "significant" against it — leading to potential false discoveries of meaningful structure
- **Static and non-growing**: Real networks grow over time; the ER/Poisson model generates a fixed-size snapshot

## Related Terms

- **[Erdos-Renyi Model](term_erdos_renyi_model.md)**: The general framework; Poisson random graph is the specific sparse regime $p = c/(n-1)$ most used in network science
- **[Random Graph](term_random_graph.md)**: The general class of probabilistic graph models
- **[Giant Component](term_giant_component.md)**: Emerges at $c = 1$ in the Poisson random graph — the most celebrated phase transition in random graph theory
- **[Degree Distribution](term_degree_distribution.md)**: Poisson in ER; the deviation of real networks from Poisson is the central motivating fact of network science
- **[Configuration Model](term_configuration_model.md)**: The degree-preserving null model — tests whether properties are explained by degree distribution alone, complementing the Poisson random graph which tests density alone
- **[Power Law](term_power_law.md)**: The fat-tailed degree distribution of real networks that the Poisson distribution cannot capture
- **[Small-World Network](term_small_world_network.md)**: Watts-Strogatz model that adds clustering to the short path lengths already present in Poisson random graphs

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Ch 4 uses Poisson random graph as the baseline for network analysis

### External Sources
- [Erdos, P. & Renyi, A. (1959). "On Random Graphs I." *Publicationes Mathematicae Debrecen*, 6, 290–297](https://snap.stanford.edu/class/cs224w-readings/erdos59random.pdf) — established the phase transition theory
- [Newman, M.E.J., Strogatz, S.H. & Watts, D.J. (2001). "Random Graphs with Arbitrary Degree Distributions and Their Applications." *Physical Review E*, 64, 026118](https://doi.org/10.1103/PhysRevE.64.026118) — generating function framework for Poisson and general degree distributions
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch 4](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — Poisson random graph as null model in the network formation framework
- [Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press](https://doi.org/10.1093/acprof:oso/9780199206650.001.0001) — comprehensive treatment of Poisson random graphs and their limitations
