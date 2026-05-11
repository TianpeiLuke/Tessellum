---
tags:
  - resource
  - terminology
  - network_science
  - social_learning
  - opinion_dynamics
keywords:
  - DeGroot learning
  - DeGroot model
  - opinion formation
  - weighted averaging
  - consensus
  - belief aggregation
  - social influence
  - naive learning
  - trust matrix
  - stochastic matrix
topics:
  - Social Learning Theory
  - Opinion Dynamics
  - Network Science
  - Belief Formation
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# DeGroot Learning

## Definition

**DeGroot learning** is a model of opinion formation on networks in which agents repeatedly update their beliefs by taking a weighted average of their own current belief and the beliefs of their neighbors. Introduced by Morris DeGroot in his 1974 paper "Reaching a Consensus," the model provides a simple, tractable framework for studying how decentralized communication in a social network can lead to consensus — or fail to do so.

Formally, let $\mathbf{x}(0) \in \mathbb{R}^n$ be the vector of initial beliefs (or opinions) of $n$ agents, and let $T$ be an $n \times n$ row-stochastic **trust matrix** where $T_{ij} \geq 0$ represents the weight agent $i$ places on agent $j$'s opinion, with $\sum_j T_{ij} = 1$ for all $i$. The update rule is:

$$\mathbf{x}(t+1) = T \cdot \mathbf{x}(t)$$

After $t$ rounds of communication, beliefs are $\mathbf{x}(t) = T^t \cdot \mathbf{x}(0)$. The central question is whether $T^t$ converges as $t \to \infty$, and if so, what the limiting beliefs are. Because $T$ is row-stochastic, the DeGroot process is mathematically equivalent to a **Markov chain** with transition matrix $T$, and convergence results from Markov chain theory apply directly.

The model is sometimes called **naive learning** because agents do not account for the fact that their neighbors' opinions may already incorporate information that was previously communicated — they simply re-average, leading to "double-counting" of initial signals. Despite this naivete, the model produces remarkably sensible aggregate outcomes under the right network conditions.

## Historical Context

Morris H. DeGroot, a Bayesian statistician at Carnegie Mellon University, proposed the model in his 1974 paper "Reaching a Consensus" (*Journal of the American Statistical Association*, 69(345), pp. 118-121). The original motivation was not social networks per se, but how a group of experts might reach agreement on a subjective probability distribution for an unknown parameter through iterated pooling of opinions.

The model received renewed attention in the 2000s when network economists recognized its power for analyzing social learning at scale. The landmark paper by Golub and Jackson (2010), "Naive Learning in Social Networks and the Wisdom of Crowds" (*American Economic Journal: Microeconomics*, 2(1), pp. 112-149), established the conditions under which DeGroot dynamics lead to correct information aggregation in large societies. Jackson's textbook *Social and Economic Networks* (2008, Chapter 8) provides the definitive treatment linking the DeGroot model to Markov chain theory, eigenvector centrality, and the Bayesian learning literature.

DeGroot's original paper contained an error in the stated convergence conditions, later corrected by Chatterjee and Seneta (1977) and Berger (1981), who established the necessary and sufficient conditions using Markov chain theory.

## Taxonomy

| Model | Update Rule | Key Feature | Outcome |
|-------|------------|-------------|---------|
| **DeGroot (1974)** | Fixed weighted averaging | Constant trust weights | Consensus (under connectivity) |
| **Friedkin-Johnsen (1990)** | Weighted average + anchoring to initial opinion | Stubbornness parameter $\lambda_i \in [0,1]$ | Persistent disagreement; no full consensus |
| **Hegselmann-Krause (Bounded Confidence)** | Average only neighbors within $\epsilon$ distance | Homophily threshold on opinion distance | Clustering into opinion groups |
| **Deffuant-Weisbuch (2000)** | Pairwise bounded confidence updates | Agents meet in random pairs | Gradual convergence to clusters |
| **Bayesian Learning on Networks** | Bayes' rule update given neighbors' actions | Fully rational, accounts for information overlap | Optimal aggregation but computationally intractable |

## Key Properties

- **Convergence condition**: Beliefs converge (i.e., $\lim_{t \to \infty} T^t$ exists) if and only if every strongly connected and closed set of agents in the trust network is aperiodic. This is equivalent to requiring that $T$ has no eigenvalues of modulus 1 other than 1 itself (within each closed communicating class).
- **Consensus condition**: All agents converge to a single shared belief if and only if the trust network is **strongly connected** (every agent can reach every other through a directed path of positive-weight links) and **aperiodic** (no cyclic structure in trust weights). Under these conditions, $T^t$ converges to a rank-one matrix.
- **Influence vector**: When consensus is reached, the common limiting belief is $x^* = \mathbf{s}' \cdot \mathbf{x}(0)$, where $\mathbf{s}$ is the **left eigenvector** of $T$ associated with eigenvalue 1 (normalized to sum to 1). The entry $s_i$ measures agent $i$'s long-run influence on the group consensus. This vector equals the **eigenvector centrality** of the agents in the trust network.
- **Influence is not expertise**: An agent's influence on the consensus depends on network position (how much others trust them, directly or indirectly), not on the accuracy of their initial signal. A poorly informed agent can dominate the consensus if they are centrally positioned.
- **Double-counting of information**: Because agents naively re-average without tracking information sources, initial beliefs that are widely shared (or held by highly connected agents) receive disproportionate weight in the consensus — a key difference from Bayesian learning.
- **Speed of convergence**: The rate of convergence to consensus is governed by the second-largest eigenvalue of $T$ (in modulus). The closer $|\lambda_2|$ is to 1, the slower convergence proceeds.
- **Markov chain equivalence**: The DeGroot process with trust matrix $T$ is mathematically identical to a Markov chain with state transition matrix $T$. The consensus belief vector $\mathbf{s}$ is the stationary distribution of this chain. All standard Markov chain results (ergodic theorem, Perron-Frobenius) apply.
- **Robustness to initial conditions**: The consensus value depends on initial beliefs through the influence vector, but the fact that consensus is reached (and the identity of who has influence) depends only on the network topology $T$.

## Notable Extensions and Models

| Extension | Authors | Key Modification | Result |
|-----------|---------|-----------------|--------|
| Wisdom of crowds conditions | Golub & Jackson (2010) | Large society limit | Correct aggregation iff max influence $\to 0$ as $n \to \infty$ |
| Friedkin-Johnsen model | Friedkin & Johnsen (1990) | Stubbornness: $\mathbf{x}(t+1) = \Lambda T \mathbf{x}(t) + (I - \Lambda) \mathbf{x}(0)$ | Disagreement persists; used to model polarization |
| Bounded confidence | Hegselmann & Krause (2002) | Trust only agents within $\epsilon$ of own opinion | Opinion clustering; fragmentation |
| Granular DeGroot | Arieli et al. (2022) | Discretize to nearest rational $1/m$ | Robust to stubborn agents and misspecification |
| Platform influence | Hkazla et al. (2022) | Personalized content injection by platform | Echo chambers from algorithmic amplification |

## Applications

| Domain | Application | Mechanism |
|--------|------------|-----------|
| **Echo chambers** | Explains how like-minded groups reinforce shared beliefs | Closed subgroups with high internal trust converge to extreme positions |
| **Polarization** | Models how network structure drives opinion divergence | Friedkin-Johnsen extension shows stubborn agents sustain disagreement |
| **Misinformation spread** | Analyzes persistence of false beliefs in networks | High-centrality misinformed agents disproportionately skew consensus |
| **Wisdom of crowds** | Conditions for accurate collective belief | Golub-Jackson: wisdom requires no single agent to dominate influence |
| **Jury deliberation** | Original DeGroot motivation: expert consensus | Iterated opinion pooling among panel members |
| **Political opinion formation** | Models voter belief evolution on social media | Trust network structure predicts who shapes public discourse |

## Challenges and Limitations

- **Naive aggregation**: Agents double-count information because they cannot distinguish fresh signals from recycled opinions. Bayesian learning avoids this but is computationally intractable on general networks.
- **Fixed trust weights**: The original model assumes trust weights never change, which is unrealistic for evolving social relationships. Adaptive-weight extensions exist but sacrifice analytical tractability.
- **Binary consensus or divergence**: The basic model either reaches full consensus or fails to converge — it cannot natively produce the stable multi-cluster opinion distributions observed in real populations (bounded confidence models address this).
- **No strategic behavior**: Agents are assumed to honestly report beliefs. In practice, agents may strategically misrepresent opinions, requiring game-theoretic extensions.
- **Homogeneous signal quality assumption**: The wisdom-of-crowds analysis assumes independent, unbiased initial signals. Correlated or systematically biased signals can lead to "confident but wrong" consensus.

## Related Terms

- **[Homophily](term_homophily.md)**: The tendency for similar individuals to connect, which shapes the trust matrix structure and can create echo chambers under DeGroot dynamics
- **[Information Cascades](term_information_cascades.md)**: A related but distinct social learning phenomenon where agents sequentially copy predecessors' actions, potentially leading everyone astray regardless of private signals
- **[PPR (Personalized PageRank)](term_ppr.md)**: A descendant of eigenvector centrality; the influence vector in DeGroot learning IS the eigenvector centrality that underlies PageRank and PPR algorithms
- **[Groupthink](term_groupthink.md)**: The psychological phenomenon of premature consensus in cohesive groups, which DeGroot dynamics can formalize through high-trust closed subnetworks
- **[Community Detection](term_community_detection.md)**: Algorithms for finding densely connected subgroups in networks; communities in the trust network correspond to opinion clusters in extended DeGroot models
- **[GNN (Graph Neural Networks)](term_gnn.md)**: Neural networks that learn on graph structures via message passing — architecturally analogous to DeGroot averaging but with learned, nonlinear aggregation functions
- **[Pairwise Stability](term_pairwise_stability.md)**: Game-theoretic equilibrium concept for network formation; the trust network in DeGroot learning is typically taken as given, but strategic formation models explain how it arises

## References

### Vault Sources

- [Digest: Social and Economic Networks (Jackson, 2008)](../digest/digest_social_economic_networks_jackson.md) — Chapter 8 provides the definitive textbook treatment of DeGroot learning, convergence conditions, and the connection to Bayesian learning
- [Acronym Glossary: Network Science](../../0_entry_points/acronym_glossary_network_science.md) — Entry point glossary containing the DeGroot learning entry and related network science terms

### External Sources

- [DeGroot, M.H. (1974). "Reaching a Consensus." *Journal of the American Statistical Association*, 69(345), 118-121.](https://doi.org/10.1080/01621459.1974.10480137) — Original paper introducing the model
- [Golub, B. & Jackson, M.O. (2010). "Naive Learning in Social Networks and the Wisdom of Crowds." *American Economic Journal: Microeconomics*, 2(1), 112-149.](https://www.aeaweb.org/articles?id=10.1257/mic.2.1.112) — Establishes conditions for correct information aggregation under DeGroot dynamics
- [Berger, R.L. (1981). "A Necessary and Sufficient Condition for Reaching a Consensus Using DeGroot's Method." *Journal of the American Statistical Association*, 76(374), 415-418.](https://www.tandfonline.com/doi/abs/10.1080/01621459.1981.10477662) — Corrects DeGroot's original convergence conditions
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch. 8.](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — Comprehensive textbook treatment linking DeGroot to Markov chains and Bayesian learning
- [Wikipedia: DeGroot Learning](https://en.wikipedia.org/wiki/DeGroot_learning) — Overview with mathematical formulation
- [MIT OCW Lecture 5: The DeGroot Learning Model (Wolitzky, 2022)](https://ocw.mit.edu/courses/14-15-networks-spring-2022/mit14_15s22_lec5.pdf) — Graduate lecture notes with proofs and examples
- [Physics of Risk: DeGroot Model](https://rf.mokslasplius.lt/degroot-model/) — Interactive simulation and intuitive explanation

---

**Last Updated**: 2026-03-15
**Status**: Active — foundational model for opinion dynamics and social learning on networks
