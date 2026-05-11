---
tags:
  - resource
  - terminology
  - network_science
  - graph_theory
  - probability_theory
  - combinatorics
keywords:
  - Erdos-Renyi
  - Erdos-Renyi model
  - G(n,p)
  - G(n,M)
  - Gilbert model
  - random graph
  - phase transition
  - sharp threshold
  - giant component
  - connectivity threshold
  - probabilistic method
topics:
  - Random Graph Theory
  - Network Science
  - Probability Theory
  - Combinatorics
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Erdos-Renyi Model

## Definition

The **Erdos-Renyi (ER) model** is the foundational mathematical framework for studying random networks. It comes in two closely related formulations:

- **$G(n, p)$ model** (Gilbert, 1959): Start with $n$ labeled vertices and include each of the $\binom{n}{2}$ possible edges independently with probability $p$. The probability of any specific graph with $m$ edges is $P(G) = p^m (1-p)^{\binom{n}{2}-m}$.

- **$G(n, M)$ model** (Erdos and Renyi, 1959): Choose uniformly at random from all graphs on $n$ labeled vertices with exactly $M$ edges.

The two formulations share asymptotic properties when $M \approx p\binom{n}{2}$. The $G(n,p)$ model is more widely used because edge independence simplifies probabilistic analysis. In the sparse regime $p = c/(n-1)$, the expected degree is $c$ and vertex degrees converge to a [Poisson distribution](term_poisson_random_graph.md) — hence "Poisson random graph."

The ER model is foundational not because it accurately describes real networks (it generally does not), but because it provides the **baseline against which all other network models are measured**. Its tractability enables exact results, and its phase transitions reveal how global structure emerges from local randomness.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1947 | **Paul Erdos** | Used random graph arguments to prove existence of graphs with high chromatic number and high girth — the first application of the probabilistic method |
| 1959 | **Paul Erdos, Alfred Renyi** | "On Random Graphs I" — introduced the $G(n,M)$ model, proved the giant component phase transition, initiated systematic study of random graph evolution |
| 1959 | **Edgar Gilbert** | Independently introduced the $G(n,p)$ model in "Random Graphs," emphasizing independent edge inclusion |
| 1960–1961 | **Erdos, Renyi** | "On the Evolution of Random Graphs" — systematically characterized thresholds for connectivity, tree components, and other structural properties |
| 1985 | **Bela Bollobas** | Published *Random Graphs*, the first comprehensive monograph consolidating two decades of results |
| 2008 | **M.O. Jackson** | Synthesized ER model within strategic network formation in *Social and Economic Networks* (Ch 4) |

## Phase Transition Thresholds

The most celebrated results in random graph theory are the **sharp thresholds** — properties that jump from probability 0 to 1 over a narrow window of $p$.

| Property | Threshold $p$ | Behavior |
|----------|--------------|----------|
| **Trees and cycles** | $p = c/n$, $c < 1$ | Components are trees and unicyclic; largest component $O(\log n)$ |
| **Giant component** | $p = 1/n$ (mean degree $c = 1$) | Supercritical ($c > 1$): unique giant component with $\Theta(n)$ vertices |
| **Connectivity** | $p = \ln(n)/n$ | Below: almost surely disconnected; above: almost surely connected |
| **Hamiltonian cycle** | $p = (\ln n + \ln \ln n)/n$ | Sharp threshold for existence of a cycle visiting every vertex |
| **Perfect matching** | $p = \ln(n)/n$ (even $n$) | Approximately coincides with connectivity threshold |

The **giant component phase transition** at $c = 1$ is the most important: below this threshold, all components have size $O(\log n)$; above it, a single giant component absorbs a macroscopic fraction $s$ of vertices satisfying $s = 1 - e^{-cs}$. At the critical point $c = 1$, the largest component scales as $n^{2/3}$.

## Key Properties

- **Edge independence**: In $G(n,p)$, edges are independent Bernoulli random variables — the defining simplification that enables most analytical results
- **Sharp thresholds**: Monotone graph properties exhibit sharp thresholds (Friedgut-Bourgain theorem) — the probability jumps from 0 to 1 over a narrow $p$-window
- **Symmetry and exchangeability**: All vertices and edges are statistically equivalent — no hubs, no communities, no spatial structure; this maximal symmetry is both the model's strength (tractability) and weakness (unrealism)
- **Branching process approximation**: Local neighborhoods resemble Galton-Watson branching processes with Poisson offspring, enabling exact computation of component size distributions
- **Small-world property**: Path lengths scale as $O(\log n / \log c)$, giving logarithmic diameter even in sparse graphs
- **Vanishing clustering**: [Clustering coefficient](term_clustering_coefficient.md) equals $p \to 0$ in sparse graphs — real networks have clustering orders of magnitude higher
- **No degree heterogeneity**: Poisson degrees cannot capture the heavy-tailed distributions ubiquitous in real networks — the primary motivation for [preferential attachment](term_preferential_attachment.md)

## Challenges and Limitations

- **No hubs**: The Poisson degree distribution has exponentially decaying tails — real networks (social, web, biological) have power-law tails with high-degree hubs
- **No clustering**: Friends of friends are no more likely to be friends than random pairs — violates the universal triadic closure pattern in social networks
- **No community structure**: ER graphs are homogeneous by construction — no dense subgroups or modular organization; the [stochastic block model](term_stochastic_block_model.md) addresses this
- **Static**: No growth or temporal dynamics; [Price model](term_price_model.md) and [preferential attachment](term_preferential_attachment.md) introduced growth as the missing ingredient
- **Unrealistic as a descriptive model**: Invaluable as a mathematical benchmark and null model, but rarely describes real systems accurately

## Related Terms

- **[Poisson Random Graph](term_poisson_random_graph.md)**: The sparse regime of the ER model where $p = c/(n-1)$ — the version most used in network science as a null model
- **[Random Graph](term_random_graph.md)**: The general class of probabilistic graph models; ER is the foundational instance
- **[Giant Component](term_giant_component.md)**: The macroscopic connected subgraph that emerges at the ER phase transition at mean degree 1
- **[Configuration Model](term_configuration_model.md)**: Extends ER by preserving a prescribed degree sequence while randomizing wiring — the next step up in null model complexity
- **[ERGM](term_ergm.md)**: Generalizes ER to capture local dependencies; ERGM with only an edge-count statistic reduces exactly to $G(n,p)$
- **[Stochastic Block Model](term_stochastic_block_model.md)**: Adds community structure to ER; SBM with $K=1$ group reduces to ER
- **[Preferential Attachment](term_preferential_attachment.md)**: Growth model producing power-law degrees — developed to address ER's inability to generate hubs

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Ch 4 covers ER model properties, phase transitions, and thresholds

### External Sources
- [Erdos, P. & Renyi, A. (1959). "On Random Graphs I." *Publicationes Mathematicae Debrecen*, 6, 290–297](https://snap.stanford.edu/class/cs224w-readings/erdos59random.pdf) — the founding paper introducing $G(n,M)$
- [Gilbert, E.N. (1959). "Random Graphs." *Annals of Mathematical Statistics*, 30(4), 1141–1144](https://doi.org/10.1214/aoms/1177706098) — independently introduced the $G(n,p)$ model
- [Bollobas, B. (2001). *Random Graphs*. 2nd ed. Cambridge University Press](https://doi.org/10.1017/CBO9780511814068) — the definitive monograph on ER random graph theory
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch 4](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — ER model within the network formation framework
