---
tags:
  - resource
  - terminology
  - network_science
  - epidemiology
  - contagion
  - diffusion
  - statistical_physics
keywords:
  - SIR model
  - Susceptible-Infected-Recovered
  - epidemic threshold
  - basic reproduction number
  - R0
  - compartmental model
  - Kermack-McKendrick
  - percolation
  - final size relation
  - epidemic spreading
topics:
  - Epidemic Modeling
  - Network Science
  - Diffusion on Networks
  - Mathematical Epidemiology
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# SIR Model (Susceptible-Infected-Recovered)

## Definition

**SIR (Susceptible-Infected-Recovered)** is a **compartmental epidemic model** that divides a population into three discrete states and describes how individuals transition between them as a disease (or behavior, information, or product) spreads. Each individual starts susceptible ($S$), may become infected ($I$) upon contact with an infected neighbor, and eventually recovers ($R$) with **permanent immunity**. The dynamics are governed by the differential equations:

$$dS/dt = -\beta SI, \quad dI/dt = \beta SI - \gamma I, \quad dR/dt = \gamma I$$

where $\beta$ is the transmission rate and $\gamma$ is the recovery rate.

The **basic reproduction number** $R_0 = \beta / \gamma$ is the expected number of secondary infections caused by a single infected individual in an otherwise susceptible population. The classical **epidemic threshold** is $R_0 = 1$: if $R_0 > 1$ an epidemic can occur; if $R_0 < 1$ the infection dies out. Because recovered individuals gain permanent immunity, SIR epidemics are self-limiting — they eventually burn out as the susceptible pool is depleted.

The critical network science contribution — by Newman (2002) — is that SIR epidemic dynamics map exactly to **[bond percolation](term_percolation_theory_networks.md)** on the contact network, where each edge is "occupied" with probability $T = 1 - e^{-\beta/\gamma}$. The final epidemic size corresponds to the [giant component](term_giant_component.md) in the percolation problem.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1927 | **W.O. Kermack, A.G. McKendrick** | Published "A Contribution to the Mathematical Theory of Epidemics," introducing the SIR model and the epidemic threshold concept; motivated by plague (London 1665) and cholera (London 1865) data |
| 1932–1933 | **Kermack, McKendrick** | Extended the theory in two follow-up papers, generalizing to age-of-infection dependence and establishing the final size relation |
| 1910s | **Ronald Ross, Hilda Hudson** | Prior work on malaria modeling that laid groundwork for compartmental approaches |
| 2002 | **M.E.J. Newman** | Established the mapping between SIR epidemics and bond percolation on networks, connecting epidemic final size to the giant component |
| 2008 | **M.O. Jackson** | Synthesized SIR within the broader framework of diffusion on networks in *Social and Economic Networks* (Chapter 7) |

## Key Properties

- **Epidemic threshold ($R_0 = 1$)**: The infection spreads if and only if $R_0 = \beta/\gamma > 1$; below this threshold the infected fraction decays exponentially
- **Self-limiting dynamics**: Because recovery confers permanent immunity, SIR epidemics always burn out — there is no endemic steady state
- **Final size relation**: The total fraction of the population eventually infected, $r_\infty$, satisfies the implicit equation $r_\infty = 1 - e^{-R_0 \cdot r_\infty}$, first derived by Kermack and McKendrick
- **SIR-percolation equivalence**: The static properties of SIR outbreaks (final size, epidemic probability) map exactly to bond percolation on the contact network, where each edge is "occupied" with probability $T = 1 - e^{-\beta/\gamma}$
- **Network heterogeneity amplifies spreading**: High-degree hubs act as super-spreaders, dramatically accelerating epidemic onset compared to homogeneous networks
- **Targeted immunization**: On [scale-free networks](term_power_law.md), vaccinating high-degree hubs is exponentially more effective than random vaccination, because removing hubs fragments the giant component

## Taxonomy (SIR Variants)

| Model | Compartments | Key Difference from SIR |
|-------|-------------|------------------------|
| **SIR** | S → I → R | Base model — permanent immunity |
| **SEIR** | S → E → I → R | Adds exposed/latent period before infectiousness |
| **SIRS** | S → I → R → S | Temporary (waning) immunity — intermediate between SIR and [SIS](term_sis_model.md) |
| **SIR on networks** | Same, transmission follows edges | Final size determined by percolation on specific graph topology |

## Applications

| Domain | Application | How SIR Is Used |
|--------|------------|-----------------|
| **Epidemiology** | Disease outbreak prediction | $R_0$ estimation guides public health interventions; final size relation predicts total infections |
| **Information diffusion** | Viral content spread on social media | SIR-like models (with "infection" = adoption) capture cascade dynamics where content "burns out" |
| **Immunization strategies** | Targeted vaccination | Network-aware SIR models reveal that targeted immunization of high-degree hubs is exponentially more effective than random vaccination on scale-free networks |
| **Product adoption** | One-time adoption cascades | SIR models capture adoption events with no repeat purchase (permanent "immunity" = already adopted) |

## Challenges and Limitations

- **Well-mixed assumption**: The classical ODE formulation assumes homogeneous mixing; network-based approaches address this but at the cost of analytical tractability
- **Static network assumption**: Most SIR network models assume the contact network is fixed, but real networks evolve concurrently with disease spread
- **Parameter estimation**: Estimating $\beta$ and $\gamma$ from real outbreak data is difficult, especially early in an epidemic
- **Binary state simplification**: Real disease dynamics involve continuous viral loads, variable infectiousness periods, and behavioral responses — compartmental models collapse these into discrete states

## Related Terms

- **[SIS Model](term_sis_model.md)**: The complementary compartmental model — SIS has no permanent immunity, allowing endemic steady states; SIR epidemics burn out, SIS epidemics can persist indefinitely
- **[Giant Component](term_giant_component.md)**: SIR epidemic final size maps to the giant component in bond percolation — the epidemic "infects" the giant component of the percolation subgraph
- **[Random Graph (Erdos-Renyi Model)](term_random_graph.md)**: The baseline network model for epidemic analysis; SIR on ER graphs recovers classical well-mixed results
- **[Degree Distribution](term_degree_distribution.md)**: Network heterogeneity in degree distribution determines epidemic threshold and spreading dynamics
- **[Power Law](term_power_law.md)**: Scale-free networks with power-law degree distributions create hub-dominated spreading and enable targeted immunization strategies
- **[Threshold Models](term_threshold_models.md)**: A complementary diffusion model using strategic (deterministic) adoption rather than probabilistic contagion
- **[Small-World Network](term_small_world_network.md)**: Small-world structure accelerates epidemic spreading relative to lattices while maintaining local clustering

- **[Exponential Distribution](term_exponential_distribution.md)**: Inter-event times in epidemic processes follow exponential distribution

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Chapter 7 covers diffusion and contagion on networks, including SIR models

### External Sources
- [Kermack, W.O. & McKendrick, A.G. (1927). "A Contribution to the Mathematical Theory of Epidemics." *Proceedings of the Royal Society A*, 115(772), 700–721](https://doi.org/10.1098/rspa.1927.0118) — the founding paper introducing the SIR model
- [Newman, M.E.J. (2002). "Spread of Epidemic Disease on Networks." *Physical Review E*, 66, 016128](https://doi.org/10.1103/PhysRevE.66.016128) — established the SIR-percolation mapping on networks
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Chapter 7](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — SIR within the broader diffusion framework
- [Wikipedia: Compartmental Models in Epidemiology](https://en.wikipedia.org/wiki/Compartmental_models_(epidemiology)) — overview of SIR and other compartmental variants
