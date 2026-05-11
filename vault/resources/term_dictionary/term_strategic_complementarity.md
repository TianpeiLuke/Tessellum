---
tags:
  - resource
  - terminology
  - network_science
  - game_theory
  - coordination_games
  - economic_theory
keywords:
  - strategic complementarity
  - strategic complementarities
  - strategic substitutability
  - strategic substitutes
  - supermodular game
  - coordination game
  - multiple equilibria
  - tipping point
  - network effects
  - technology adoption
topics:
  - Network Science
  - Game Theory on Networks
  - Coordination Games
  - Economic Theory
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Strategic Complementarity

## Definition

**Strategic complementarity** is a property of a game in which a player's incentive to take an action (or to increase the level of an action) is **increasing** in the actions of other players. Formally, actions are strategic complements when the best-response function of each player is monotonically increasing in the actions of rivals -- i.e., when others do more of something, each agent's marginal benefit from doing the same thing rises. This is the defining feature of **supermodular games**, as formalized by Topkis (1979) and further developed by Vives (1990).

The converse concept is **strategic substitutability**, where a player's incentive to act *decreases* when others act. In the network context studied by Jackson (2008, Ch. 9), these two regimes produce fundamentally different equilibrium structures: complementarity drives coordination and cascading adoption, while substitutability drives specialization and free-riding.

Strategic complementarity is the formal mechanism underlying many phenomena in network science: technology adoption cascades, bank runs, currency attacks, crime contagion, and coordination failures in public goods provision. When complementarity is strong enough that individual reactions to aggregate changes are more than one-for-one, **multiple equilibria** emerge -- and which equilibrium is reached depends critically on network topology and initial conditions.

## Historical Context

The term "strategic complements" was coined by **Bulow, Geanakoplos, and Klemperer (1985)** in their paper "Multimarket Oligopoly: Strategic Substitutes and Complements" published in the *Journal of Political Economy*. They distinguished between markets where firms' strategies reinforce each other (complements, e.g., Bertrand price competition) versus offset each other (substitutes, e.g., Cournot quantity competition).

The mathematical foundations were laid by **Topkis (1979)** through the theory of supermodular functions on lattices, and later refined by **Vives (1990)** who connected supermodularity to monotone comparative statics in games. **Milgrom and Roberts (1990)** extended the framework in their influential paper "Rationalizability, Learning, and Equilibrium in Games with Strategic Complementarities," showing that supermodular games have extremal Nash equilibria computable via iterated best response.

**Jackson (2008)** integrated strategic complementarity into the network science framework in *Social and Economic Networks* (Chapter 9), demonstrating how network topology determines threshold behavior, cascade dynamics, and which equilibria are reachable under complementarity and substitutability.

## Taxonomy

| Type | Best Response | Network Effect | Canonical Example |
|------|--------------|----------------|-------------------|
| **Strategic Complementarity** | Increasing in neighbors' actions | Positive feedback; cascading adoption | Technology adoption, bank runs, protest participation |
| **Strategic Substitutability** | Decreasing in neighbors' actions | Negative feedback; specialization | Public goods provision, security investment, vaccination |
| **Mixed / Heterogeneous** | Varies by agent or action | Context-dependent | Markets with both network effects and congestion |

### Complementarity vs. Substitutability on Networks

| Property | Complementarity | Substitutability |
|----------|----------------|-------------------|
| **Equilibrium structure** | Multiple equilibria; coordination problem | Tends toward unique equilibrium; specialization |
| **Role of network density** | Denser networks facilitate cascades | Denser networks enable more free-riding |
| **Key challenge** | Selecting among equilibria; avoiding bad coordination traps | Ensuring sufficient provision despite free-riding |
| **Tipping behavior** | Strong tipping points; S-curve adoption | Gradual adjustment; no sharp tipping |
| **Policy lever** | Seed critical mass in well-connected nodes | Target peripheral nodes who under-contribute |

## Key Properties

- **Supermodularity**: Strategic complementarity is mathematically equivalent to the game's payoff function being supermodular -- the cross-partial derivative $\frac{\partial^2 u_i}{\partial a_i \partial a_j} \geq 0$ for all pairs of players $i, j$.
- **Monotone best responses**: Each player's best-response function is non-decreasing in the actions of others, ensuring the existence of extremal (greatest and least) pure-strategy Nash equilibria.
- **Multiple equilibria**: When complementarity is sufficiently strong, the game exhibits multiple Nash equilibria -- typically a "high-activity" equilibrium and a "low-activity" equilibrium, with potentially many intermediate ones.
- **Tipping points and critical mass**: Adoption dynamics exhibit threshold behavior; once a sufficient fraction of neighbors adopt (the tipping point), cascading adoption becomes self-sustaining. The critical threshold depends on network structure.
- **Path dependence**: History and initial conditions determine which equilibrium is reached, making early-mover advantages and network seeding strategically important.
- **Network topology dependence**: The set of reachable equilibria depends on degree distribution, clustering, and community structure. Hub nodes are disproportionately important for triggering cascades.
- **Contagion and diffusion**: Under complementarity, behaviors spread through networks analogously to epidemic contagion, with network thresholds playing the role of infection thresholds.
- **Comparative statics via lattice theory**: The lattice structure of the strategy space allows powerful comparative statics results -- increasing a parameter that raises all payoffs shifts both extremal equilibria upward.

## Notable Systems / Implementations

| Domain | System / Phenomenon | Complementarity Mechanism |
|--------|---------------------|--------------------------|
| **Technology adoption** | Platform/network goods (fax, email, social media) | Value of adopting increases with number of adopters (network externalities) |
| **Financial contagion** | Bank runs (Diamond-Dybvig model) | Incentive to withdraw increases as more depositors withdraw |
| **Crime networks** | Criminal activity in neighborhoods | Returns to crime increase when neighbors also engage in crime (reduced enforcement per capita) |
| **Social movements** | Protest participation (Granovetter threshold model) | Willingness to protest increases with expected turnout |
| **Digital payments** | P2P payment platforms (Venmo, UPI) | Utility of adoption increases with fraction of contacts using the platform |

## Applications

| Application Area | Role of Complementarity | Key Network Consideration |
|-----------------|------------------------|--------------------------|
| **Industrial organization** | Firms' pricing or R&D strategies reinforce each other | Market structure determines strategic interaction mode |
| **Public policy / nudges** | Seeding adoption in high-centrality nodes triggers cascades | Target network hubs to maximize diffusion |
| **Epidemiology analogies** | Behavioral adoption modeled as contagion with thresholds | Degree distribution determines cascade threshold |
| **Mechanism design** | Design incentives to shift equilibrium selection | Network-aware subsidies can tip systems to high-activity equilibrium |
| **Security and crime** | Substitutability in security provision leads to under-investment | Free-riding on neighbors' security investments |

## Challenges and Limitations

- **Equilibrium selection problem**: Complementarity generates multiple equilibria but does not predict which one will be realized; additional refinements (risk dominance, stochastic stability) are needed.
- **Observability of network structure**: Optimal policy (e.g., whom to subsidize for adoption) requires knowledge of the full network, which is rarely available.
- **Heterogeneous thresholds**: Real agents have different thresholds for adoption, complicating the clean complementarity/substitutability dichotomy.
- **Dynamic complexity**: Static supermodular game results do not always extend to dynamic settings with learning, adjustment costs, and evolving networks.
- **Mixed incentive environments**: Many real-world settings exhibit complementarity for some actions and substitutability for others simultaneously.

## Related Terms

- **[Game Theory](term_game_theory.md)**: The broader framework within which strategic complementarity is defined; complementarity determines the structure of best responses and equilibria
- **[Pairwise Stability](term_pairwise_stability.md)**: Network formation equilibrium concept; the networks that form under pairwise stability then serve as the substrate on which complementarity/substitutability games are played
- **[Network Centrality](term_network_centrality.md)**: Centrality measures identify the nodes most influential for triggering cascades under complementarity
- **[Information Cascades](term_information_cascades.md)**: A related contagion phenomenon where sequential rational imitation produces herding; complementarity provides a game-theoretic foundation for similar cascading dynamics

## References

### Vault Sources

### External Sources
- [Bulow, Geanakoplos & Klemperer (1985). "Multimarket Oligopoly: Strategic Substitutes and Complements." *Journal of Political Economy*, 93(3), 488-511](https://www.jstor.org/stable/1832005) -- seminal paper coining the terms "strategic complements" and "strategic substitutes"
- [Topkis (1979). "Equilibrium Points in Nonzero-Sum n-Person Submodular Games." *SIAM Journal on Control and Optimization*, 17(6), 773-787](https://epubs.siam.org/doi/10.1137/0317054) -- mathematical foundations of supermodular games on lattices
- [Vives (1990). "Nash Equilibrium with Strategic Complementarities." *Journal of Mathematical Economics*, 19(3), 305-321](https://www.sciencedirect.com/science/article/abs/pii/030440689090005T) -- formal development of complementarity in game-theoretic settings
- [Milgrom & Roberts (1990). "Rationalizability, Learning, and Equilibrium in Games with Strategic Complementarities." *Econometrica*, 58(6), 1255-1277](https://www.jstor.org/stable/2938316) -- extremal equilibria and comparative statics in supermodular games
- [Jackson (2008). *Social and Economic Networks*, Chapter 9. Princeton University Press](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) -- network games with complementarity and substitutability, threshold models, and diffusion
- [Wikipedia: Strategic Complements](https://en.wikipedia.org/wiki/Strategic_complements) -- overview of strategic complements and substitutes
