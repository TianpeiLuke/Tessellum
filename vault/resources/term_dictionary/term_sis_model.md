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
  - SIS model
  - Susceptible-Infected-Susceptible
  - epidemic threshold
  - basic reproduction number
  - R0
  - compartmental model
  - endemic steady state
  - scale-free networks
  - vanishing threshold
  - Pastor-Satorras
  - Vespignani
  - spectral condition
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

# SIS Model (Susceptible-Infected-Susceptible)

## Definition

**SIS (Susceptible-Infected-Susceptible)** is a **compartmental epidemic model** where individuals cycle between susceptible ($S$) and infected ($I$) states — there is **no permanent immunity**. After recovering from infection, individuals return to the susceptible pool and can be reinfected. This creates the possibility of an **endemic steady state** where a constant fraction of the population remains infected indefinitely, in contrast to the [SIR model](term_sir_model.md) where epidemics always burn out.

The dynamics are governed by:

$$dS/dt = \gamma I - \beta SI, \quad dI/dt = \beta SI - \gamma I$$

where $\beta$ is the transmission rate and $\gamma$ is the recovery rate. The **basic reproduction number** $R_0 = \beta / \gamma$ determines whether the infection persists: if $R_0 > 1$, the system reaches an endemic equilibrium; if $R_0 < 1$, the infection dies out.

The landmark network science result — by **Pastor-Satorras and Vespignani (2001)** — is that on [scale-free networks](term_power_law.md) with diverging second moment of the [degree distribution](term_degree_distribution.md), the **SIS epidemic threshold approaches zero**: $\lambda_c \to 0$. This means that **any disease with any positive transmission rate can become endemic** on a scale-free network. This result has profound implications for understanding why computer viruses, misinformation, and certain behaviors persist on real-world networks despite low individual transmission rates.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1927 | **W.O. Kermack, A.G. McKendrick** | Established the compartmental modeling framework; SIS is the natural variant of their SIR model for diseases without lasting immunity |
| 2000–2001 | **R. Pastor-Satorras, A. Vespignani** | Demonstrated the absence of an epidemic threshold for SIS dynamics on scale-free networks (*Physical Review Letters*, 2001) — the central result linking epidemic models to network topology |
| 2003 | **R. Pastor-Satorras, A. Vespignani** | Extended the analysis to show that the SIS threshold on any network is determined by the largest eigenvalue of the adjacency matrix |
| 2008 | **M.O. Jackson** | Synthesized SIS within the broader framework of diffusion on networks in *Social and Economic Networks* (Chapter 7) |
| 2015 | **Pastor-Satorras, Castellano, Van Mieghem, Vespignani** | Comprehensive review in *Reviews of Modern Physics* consolidating two decades of epidemic processes on complex networks |

## Key Properties

- **No permanent immunity**: Recovered individuals return to the susceptible pool, enabling reinfection and persistent endemic states
- **Endemic steady state**: When $R_0 > 1$, the SIS model reaches a stationary state where a constant fraction $i^* = 1 - 1/R_0$ of the population remains infected
- **Vanishing threshold on scale-free networks**: For SIS dynamics on networks with power-law degree distribution $P(k) \sim k^{-\alpha}$ where $2 < \alpha \leq 3$, the epidemic threshold $\lambda_c \to 0$ as network size $N \to \infty$, because $\langle k \rangle / \langle k^2 \rangle \to 0$
- **Spectral condition**: On a general network, the SIS epidemic threshold is $\lambda_c = 1/\lambda_1$, where $\lambda_1$ is the largest eigenvalue of the adjacency matrix
- **Mean-field approximation**: On random graphs, SIS dynamics can be approximated by heterogeneous mean-field theory, yielding $\lambda_c = \langle k \rangle / \langle k^2 \rangle$
- **Network heterogeneity amplifies persistence**: High-degree hubs sustain infection even at low transmission rates, acting as persistent reservoirs
- **Contact process analog**: SIS on networks is the discrete analog of the contact process from statistical physics, sharing universality class properties near the critical point

## Taxonomy (SIS Variants)

| Model | Compartments | Key Difference from SIS |
|-------|-------------|------------------------|
| **SIS** | S → I → S | Base model — no immunity, endemic equilibrium possible |
| **SIR** | S → I → R | Permanent immunity — epidemics burn out (see [SIR Model](term_sir_model.md)) |
| **SIRS** | S → I → R → S | Temporary (waning) immunity — intermediate between SIS and SIR |
| **SIS on networks** | Same, transmission follows edges | Threshold depends on spectral properties of adjacency matrix |

## Applications

| Domain | Application | How SIS Is Used |
|--------|------------|-----------------|
| **Computer virus propagation** | Internet security | SIS on the Internet topology (scale-free) explains why computer viruses persist at arbitrarily low infection rates — the vanishing threshold means eradication requires vaccinating hubs |
| **Financial contagion** | Systemic risk in banking networks | SIS-like models on interbank networks capture how defaults cascade and persist through the financial system |
| **Misinformation persistence** | Social media dynamics | SIS models explain why false information persists despite low per-contact transmission — reinfection (re-exposure) keeps it endemic |
| **Recurring behaviors** | Habit adoption and relapse | SIS captures behaviors without permanent adoption — users can adopt, lapse, and re-adopt (e.g., app usage patterns) |

## Challenges and Limitations

- **Well-mixed assumption**: The classical ODE formulation assumes homogeneous mixing; network-based approaches address this but at the cost of analytical tractability
- **Static network assumption**: Most SIS network models assume the contact network is fixed, but real networks evolve concurrently with contagion
- **Mean-field limitations**: Heterogeneous mean-field and quenched mean-field approximations can be inaccurate near the epidemic threshold, particularly for networks with strong degree correlations or community structure
- **Parameter estimation**: Estimating $\beta$ and $\gamma$ is difficult for non-biological contagion (information, behaviors) where "infection" and "recovery" are not sharply defined
- **Binary state simplification**: Real contagion dynamics involve continuous states of engagement or susceptibility, not binary infected/susceptible

## Related Terms

- **[SIR Model](term_sir_model.md)**: The complementary compartmental model — SIR has permanent immunity so epidemics burn out; SIS allows reinfection and endemic persistence
- **[Degree Distribution](term_degree_distribution.md)**: The key network property governing SIS epidemic thresholds; the ratio $\langle k \rangle / \langle k^2 \rangle$ determines whether the threshold vanishes
- **[Power Law](term_power_law.md)**: Scale-free networks with power-law degree distributions $P(k) \sim k^{-\alpha}$ have diverging $\langle k^2 \rangle$ for $\alpha \leq 3$, causing the SIS epidemic threshold to vanish — the central result of Pastor-Satorras and Vespignani
- **[Preferential Attachment](term_preferential_attachment.md)**: The growth mechanism that generates scale-free networks; the resulting hub-dominated topology is what causes the vanishing SIS threshold
- **[Random Graph (Erdos-Renyi Model)](term_random_graph.md)**: The baseline network model; SIS on ER graphs has a finite positive epidemic threshold because the Poisson degree distribution has finite second moment
- **[Community Detection](term_community_detection.md)**: Modular network structure affects SIS dynamics — communities create local containment and delayed inter-community transmission
- **[Network Centrality](term_network_centrality.md)**: Centrality measures identify the most influential spreaders and persistent reservoirs in SIS dynamics

- **[Exponential Distribution](term_exponential_distribution.md)**: SIS recovery/infection times are exponentially distributed

## References

### Vault Sources
- [Digest: Social and Economic Networks — Jackson](../digest/digest_social_economic_networks_jackson.md) — Chapter 7 covers diffusion and contagion on networks, including SIS models

### External Sources
- [Pastor-Satorras, R. & Vespignani, A. (2001). "Epidemic Spreading in Scale-Free Networks." *Physical Review Letters*, 86(14), 3200–3203](https://doi.org/10.1103/PhysRevLett.86.3200) — proved the absence of an epidemic threshold for SIS dynamics on scale-free networks
- [Pastor-Satorras, R., Castellano, C., Van Mieghem, P. & Vespignani, A. (2015). "Epidemic Processes in Complex Networks." *Reviews of Modern Physics*, 87(3), 925–979](https://doi.org/10.1103/RevModPhys.87.925) — comprehensive review covering SIS mean-field theories, exact results, and simulations
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Chapter 7](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — SIS within the broader diffusion framework
- [Wikipedia: Compartmental Models in Epidemiology](https://en.wikipedia.org/wiki/Compartmental_models_(epidemiology)) — overview of SIS and other compartmental variants
