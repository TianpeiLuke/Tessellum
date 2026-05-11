---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - probability_theory
  - combinatorics
keywords:
  - random graph
  - random network
  - probabilistic graph model
  - network model
  - graph ensemble
  - null model
topics:
  - Random Graph Theory
  - Network Science
  - Probability Theory
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Random Graph

## Definition

A **random graph** is a graph constructed by a stochastic process that determines which edges are present. The term encompasses a family of probabilistic models, each capturing different structural features of real networks. Random graph models serve two roles in network science: as **null models** (baselines for testing whether observed properties are non-random) and as **generative models** (mechanisms explaining how networks form).

The field was founded by Erdos, Renyi, and Gilbert in 1959 with the simplest possible random graph — each edge included independently with fixed probability. Since then, progressively richer models have been developed to capture features that the basic model cannot: fat-tailed degree distributions, clustering, community structure, and growth dynamics.

## Taxonomy of Random Graph Models

| Model | Mechanism | Degree Distribution | What It Captures | What It Misses |
|-------|-----------|-------------------|-----------------|----------------|
| **[Erdos-Renyi $G(n,p)$](term_erdos_renyi_model.md)** | Independent edge inclusion with probability $p$ | [Poisson](term_poisson_random_graph.md) | Phase transitions; short path lengths | Hubs, clustering, communities |
| **[Configuration Model](term_configuration_model.md)** | Prescribed degree sequence, random wiring | Arbitrary (input) | Any degree distribution | Clustering, communities, correlations |
| **[Stochastic Block Model](term_stochastic_block_model.md)** | Edge probability depends on group membership | Mixture | Community structure | Degree heterogeneity (without DC-SBM) |
| **[ERGM](term_ergm.md)** | Exponential family over graph statistics | Depends on specification | Triangles, reciprocity, homophily | Computational tractability at scale |
| **[Price Model](term_price_model.md)** | Directed growth + cumulative advantage | Power law (in-degree) | Citation networks; directed hubs | Undirected networks; clustering |
| **[Preferential Attachment (BA)](term_preferential_attachment.md)** | Undirected growth + degree-proportional attachment | Power law $P(k) \sim k^{-3}$ | Scale-free hubs | Clustering, tunable exponent |
| **[Small World (Watts-Strogatz)](term_small_world_network.md)** | Regular lattice + random rewiring | Peaked (near-regular) | High clustering + short paths | Degree heterogeneity |
| **Chung-Lu** | Edge probability $\propto w_i w_j$ | Arbitrary (prescribed) | Degree heterogeneity | Clustering, communities |

## Null Model Hierarchy

Random graph models form a hierarchy of increasingly constrained null models:

| Level | Null Model | What Is Preserved | What Is Randomized | Tests Whether... |
|-------|-----------|-------------------|-------------------|-----------------|
| 0 | [Erdos-Renyi](term_erdos_renyi_model.md) / [Poisson](term_poisson_random_graph.md) | Edge count (density) | Everything else | ...the property is explained by density alone |
| 1 | [Configuration Model](term_configuration_model.md) | Degree sequence | Wiring pattern | ...the property is explained by degree distribution |
| 2 | [Stochastic Block Model](term_stochastic_block_model.md) | Group structure + density | Within/between-group wiring | ...the property is explained by community structure |
| 3 | [ERGM](term_ergm.md) | Specified local statistics | Global structure | ...the property is explained by local dependencies |

## Key Properties (Shared Across Models)

- **Phase transitions**: Most random graph models exhibit sharp thresholds where qualitative properties (connectivity, giant component) emerge abruptly at critical parameter values
- **Probabilistic method**: Random graphs enable existence proofs — showing that graphs with specific properties exist by demonstrating they occur with positive probability in the random ensemble
- **Mean-field analyzability**: Locally tree-like random graphs permit exact mean-field solutions for dynamical processes ([SIR](term_sir_model.md), [SIS](term_sis_model.md), [percolation](term_percolation_theory_networks.md))
- **Asymptotic universality**: Many properties depend on the model only through a few summary statistics (mean degree, degree variance, clustering) in the large-$n$ limit

## Related Terms

- **[Erdos-Renyi Model](term_erdos_renyi_model.md)**: The foundational random graph — $G(n,p)$ and $G(n,M)$ formulations, phase transition thresholds, sharp threshold phenomena
- **[Poisson Random Graph](term_poisson_random_graph.md)**: The sparse ER regime $p = c/(n-1)$ — the canonical null model in network science with Poisson degree distribution
- **[Configuration Model](term_configuration_model.md)**: Degree-preserving null model — random wiring with prescribed degree sequence
- **[Stochastic Block Model](term_stochastic_block_model.md)**: Community-aware random graph — edge probabilities depend on group membership
- **[ERGM](term_ergm.md)**: Statistical random graph model capturing local dependencies via exponential family
- **[Price Model](term_price_model.md)**: Directed growth model with cumulative advantage — the first preferential attachment model
- **[Preferential Attachment](term_preferential_attachment.md)**: Undirected growth model producing scale-free networks
- **[Giant Component](term_giant_component.md)**: The macroscopic connected subgraph emerging at the phase transition
- **[Degree Distribution](term_degree_distribution.md)**: The key structural statistic distinguishing random graph models
- **[Small-World Network](term_small_world_network.md)**: Watts-Strogatz model adding clustering to random graph short paths

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Ch 3-5 cover random graph models as foundations for network analysis

### External Sources
- [Erdos, P. & Renyi, A. (1959). "On Random Graphs I." *Publicationes Mathematicae Debrecen*, 6, 290–297](https://snap.stanford.edu/class/cs224w-readings/erdos59random.pdf) — founding paper of random graph theory
- [Bollobas, B. (2001). *Random Graphs*. 2nd ed. Cambridge University Press](https://doi.org/10.1017/CBO9780511814068) — definitive monograph
- [Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press](https://doi.org/10.1093/acprof:oso/9780199206650.001.0001) — comprehensive textbook covering all major random graph models
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — random graph models in the economic network formation framework
