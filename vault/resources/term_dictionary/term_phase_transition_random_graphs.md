---
tags:
  - resource
  - terminology
  - network_science
  - random_graph_theory
  - graph_theory
  - statistical_physics
  - percolation_theory
  - combinatorics
keywords:
  - phase transition
  - sharp threshold
  - critical threshold
  - giant component transition
  - connectivity threshold
  - percolation
  - subcritical regime
  - supercritical regime
  - critical window
  - Molloy-Reed criterion
  - epidemic threshold
  - monotone graph property
topics:
  - Random Graph Theory
  - Network Science
  - Statistical Physics
  - Percolation Theory
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Phase Transition in Random Graph Theory

## Definition

A **phase transition** in random graph theory is an abrupt qualitative change in the structural properties of a random graph as a parameter (typically edge probability $p$ or mean degree $c$) crosses a critical value. Below the critical value, a property holds with probability tending to 0; above it, the property holds with probability tending to 1. The transition occurs over a vanishingly narrow parameter window relative to the parameter range — this is what makes it "sharp" rather than gradual.

The concept is borrowed from statistical physics, where phase transitions describe discontinuous changes in material properties (e.g., water freezing at 0°C). In graphs, the analogous phenomenon is that global topological properties — connectivity, existence of a giant component, Hamiltonicity — emerge suddenly as local connection probabilities increase. The [Erdos-Renyi model](term_erdos_renyi_model.md) $G(n,p)$ provides the cleanest setting: edges are independent Bernoulli random variables, and sharp thresholds arise from the collective behavior of $\binom{n}{2}$ independent coin flips.

Jackson (2008, Ch 4) emphasizes that phase transitions explain when networks "work" — a [giant component](term_giant_component.md) enables diffusion, communication, and coordination across a population — versus when they "fail" — fragmentation under attack or insufficient connectivity prevents global reach.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1957 | **Broadbent, Hammersley** | Introduced percolation theory — the physics framework for phase transitions on lattices |
| 1959–1961 | **Erdos, Renyi** | Discovered the giant component phase transition at $c = 1$ and connectivity threshold at $p = \ln(n)/n$ in random graphs |
| 1959 | **Gilbert** | Independently introduced $G(n,p)$, the model where phase transitions are most naturally studied |
| 1985/2001 | **Bollobas** | Systematized random graph thresholds in *Random Graphs*; rigorous treatment of the critical window |
| 1996 | **Molloy, Reed** | Extended the giant component phase transition to random graphs with arbitrary degree sequences (configuration model) |
| 1999 | **Friedgut, Kalai** | Proved that every monotone graph property has a sharp threshold — a universal phase transition theorem |
| 2001 | **Pastor-Satorras, Vespignani** | Showed the epidemic threshold vanishes on scale-free networks — a phase transition that disappears |
| 2008 | **Jackson** | Synthesized phase transitions within social and economic network theory (Ch 4) |

## The Giant Component Transition (c = 1)

The most celebrated phase transition in random graph theory occurs in the [Erdos-Renyi model](term_erdos_renyi_model.md) $G(n, p)$ with $p = c/n$:

| Regime | Mean Degree | Largest Component | Structure |
|--------|-------------|-------------------|-----------|
| **Subcritical** | $c < 1$ | $O(\log n)$ | All components are trees or unicyclic; network is fragmented |
| **Critical** | $c = 1$ | $\Theta(n^{2/3})$ | The critical window; components begin to merge; largest component scales as $n^{2/3}$ |
| **Supercritical** | $c > 1$ | $\Theta(n)$ | A unique [giant component](term_giant_component.md) contains fraction $s$ of vertices, where $s = 1 - e^{-cs}$ |

At $c = 1$, the transition is continuous (second-order): the giant component fraction grows continuously from 0, unlike a discontinuous (first-order) jump. The critical window has width $O(n^{-1/3})$ around $c = 1$.

The giant component is directly analogous to the infinite cluster in **bond percolation** on the complete graph $K_n$: retaining each edge with probability $p = c/n$ is exactly bond percolation with that retention probability. This connection to [percolation theory](term_percolation_theory_networks.md) in statistical physics provides the deep mathematical tools (branching process approximation, generating functions) that make exact analysis possible.

## Other Major Thresholds

| Property | Threshold $p$ | Significance |
|----------|--------------|-------------|
| **Connectivity** | $p = \ln(n)/n$ | Below: isolated vertices persist, graph disconnected; above: graph almost surely connected |
| **Hamiltonian cycle** | $p = (\ln n + \ln \ln n)/n$ | Sharp threshold for visiting every vertex in a single cycle |
| **$k$-connectivity** | $p = (\ln n + (k-1)\ln \ln n)/n$ | Threshold for minimum vertex cut of size $k$ |
| **Perfect matching** | $p \approx \ln(n)/n$ | Approximately coincides with connectivity (for even $n$) |
| **Chromatic number** | Depends on $c$ | Sharp transitions in colorability at specific average degrees |

## Key Properties

- **Sharp thresholds (Friedgut-Kalai theorem)**: Every monotone graph property has a sharp threshold — the probability jumps from $\varepsilon$ to $1 - \varepsilon$ over a window of width $O(1/\log n)$ in $p$. A property is monotone if adding edges cannot destroy it (e.g., connectivity, containing a triangle, having a giant component)
- **Universality**: Phase transitions are not artifacts of the ER model — they appear in the [configuration model](term_configuration_model.md) (Molloy-Reed criterion), [stochastic block model](term_stochastic_block_model.md) (detectability threshold), and virtually all random graph families
- **Branching process duality**: Near the critical point, local neighborhoods of a random vertex approximate a Galton-Watson branching process with Poisson($c$) offspring; the giant component exists iff this branching process survives with positive probability
- **Percolation equivalence**: The ER model $G(n, c/n)$ is mathematically equivalent to bond percolation on the complete graph $K_n$ with retention probability $c/n$; this maps random graph theory onto the vast machinery of percolation theory from statistical physics
- **Critical scaling**: At $c = 1$, the largest component has $\Theta(n^{2/3})$ vertices and $\Theta(n^{2/3})$ excess edges — a fractal-like structure that is neither tree-like (subcritical) nor dense (supercritical)
- **Asymptotic almost sure (a.a.s.)**: Phase transition results hold with probability tending to 1 as $n \to \infty$; for any fixed $n$, there is a nonzero probability of deviation from the asymptotic behavior

## Phase Transitions in Other Models

| Model | Phase Transition | Criterion |
|-------|-----------------|-----------|
| **[Configuration Model](term_configuration_model.md)** | Giant component emergence | **Molloy-Reed criterion**: $\sum_k k(k-2)p_k > 0$, i.e., $\langle k^2 \rangle > 2\langle k \rangle$; depends on degree variance, not just mean |
| **[Stochastic Block Model](term_stochastic_block_model.md)** | Community detectability | Below the Kesten-Stigum threshold, no algorithm can detect communities better than random guessing |
| **Scale-free networks** | [SIS](term_sis_model.md) epidemic threshold | Threshold vanishes: $\lambda_c \to 0$ as $n \to \infty$ for power-law exponent $\gamma \leq 3$ (Pastor-Satorras & Vespignani 2001) |
| **[SIR](term_sir_model.md) on networks** | Epidemic outbreak | Final epidemic size maps to giant component of bond-percolated network; threshold at $R_0 = 1$ |
| **Network resilience** | Percolation under attack | Random failure: scale-free networks are robust (threshold near $p_c = 1$); targeted attack on hubs: catastrophic fragmentation at low removal fractions |

## Applications

| Domain | Phase Transition | Implication |
|--------|-----------------|-------------|
| **Epidemiology** | Epidemic threshold ($R_0 = 1$) | Below threshold, outbreaks die out; above, epidemics spread to a macroscopic fraction; network structure determines $R_0$ |
| **Network resilience** | Percolation threshold under node/edge removal | Scale-free networks survive random failures but collapse under targeted hub removal — a phase transition in robustness |
| **Information diffusion** | Giant component as diffusion backbone | Information, innovation, or behavior can only spread globally when a giant component exists — Jackson's key insight about when networks "work" |
| **Cascading failures** | Threshold for cascade propagation | In threshold models, a critical seed size triggers global adoption; network topology determines whether cascades fizzle or explode |
| **Infrastructure** | Power grid / internet connectivity | Phase transitions predict when incremental failures trigger system-wide collapse |

## Challenges and Limitations

- **Finite-size effects**: Sharp thresholds are asymptotic ($n \to \infty$) results; real networks are finite, so transitions are smoothed into crossovers rather than sharp jumps
- **Model dependence**: The precise threshold value depends on the random graph model; real networks rarely match any single model's assumptions
- **Correlated edges**: Most sharp threshold results assume edge independence; real networks have correlations (clustering, degree-degree correlations) that can shift or smear thresholds
- **Dynamic networks**: Phase transition theory assumes a static snapshot; real networks evolve, so the system may never reach the steady state assumed by threshold results
- **Heterogeneous thresholds**: In models with node-level variation (heterogeneous SIR, strategic threshold models), the simple "one critical value" picture breaks down into more complex phase diagrams

## Related Terms
- **[Erdos-Renyi Model](term_erdos_renyi_model.md)**: The primary random graph model where phase transitions were first discovered and most thoroughly studied
- **[Poisson Random Graph](term_poisson_random_graph.md)**: The sparse ER regime $p = c/(n-1)$ where the giant component transition occurs at $c = 1$
- **[Giant Component](term_giant_component.md)**: The most important phase transition outcome — a connected subgraph containing $\Theta(n)$ vertices
- **[Random Graph](term_random_graph.md)**: General umbrella class of probabilistic graph models exhibiting various phase transitions
- **[Configuration Model](term_configuration_model.md)**: Phase transition governed by the Molloy-Reed criterion $\langle k^2 \rangle > 2\langle k \rangle$
- **[SIR Model](term_sir_model.md)**: Epidemic threshold at $R_0 = 1$ is a phase transition; final size maps to bond percolation
- **[SIS Model](term_sis_model.md)**: Epidemic threshold vanishes on scale-free networks — a qualitatively different phase transition behavior
- **[Stochastic Block Model](term_stochastic_block_model.md)**: Detectability threshold as a phase transition in community recovery
- **[Degree Distribution](term_degree_distribution.md)**: Determines critical thresholds via the Molloy-Reed criterion; fat tails shift or eliminate thresholds
- **[Power Law](term_power_law.md)**: Scale-free degree distributions fundamentally alter phase transition behavior (vanishing epidemic thresholds, resilience asymmetry)

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Ch 4 covers random graph phase transitions, giant component emergence, and connectivity thresholds

### External Sources
- [Erdos, P. & Renyi, A. (1960). "On the Evolution of Random Graphs." *Magyar Tud. Akad. Mat. Kutato Int. Kozl.*, 5, 17–61](https://www.renyi.hu/~p_erdos/1961-15.pdf) — systematic treatment of phase transitions and thresholds in random graphs
- [Bollobas, B. (2001). *Random Graphs*. 2nd ed. Cambridge University Press](https://doi.org/10.1017/CBO9780511814068) — the definitive monograph covering all major phase transitions
- [Molloy, M. & Reed, B. (1995). "A Critical Point for Random Graphs with a Given Degree Sequence." *Random Structures & Algorithms*, 6(2-3), 161–180](https://doi.org/10.1002/rsa.3240060204) — the Molloy-Reed criterion for giant components in configuration models
- [Friedgut, E. & Kalai, G. (1996). "Every Monotone Graph Property Has a Sharp Threshold." *Proc. AMS*, 124(10), 2993–3002](https://www.ams.org/jams/1999-12-04/S0894-0347-99-00305-7/S0894-0347-99-00305-7.pdf) — universal sharp threshold theorem for monotone properties
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch 4](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — phase transitions within the social and economic network framework
- [Wikipedia: Giant Component](https://en.wikipedia.org/wiki/Giant_component) — accessible overview of the giant component phase transition
