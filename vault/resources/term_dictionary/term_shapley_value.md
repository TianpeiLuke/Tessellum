---
tags:
  - resource
  - terminology
  - cooperative_game_theory
  - network_science
  - economics
  - fair_allocation
  - explainable_ai
keywords:
  - Shapley value
  - cooperative game theory
  - coalition game
  - marginal contribution
  - fair allocation
  - SHAP
  - Myerson value
  - Banzhaf power index
  - cost sharing
  - voting power
  - feature importance
topics:
  - Cooperative Game Theory
  - Fair Allocation and Mechanism Design
  - Network Science
  - ML Interpretability
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Shapley Value

## Definition

The **Shapley value** is a solution concept in cooperative game theory that assigns a unique payoff to each player in a coalitional game based on their average marginal contribution across all possible orderings of players. Given a coalitional game $(N, v)$ where $N$ is a finite set of $n$ players and $v : 2^N \to \mathbb{R}$ is a characteristic function with $v(\emptyset) = 0$, the Shapley value of player $i$ is:

$$\phi_i(N, v) = \frac{1}{n!} \sum_{S \subseteq N \setminus \{i\}} |S|! \cdot (n - |S| - 1)! \cdot \bigl[v(S \cup \{i\}) - v(S)\bigr]$$

Intuitively, the formula considers every possible ordering (permutation) in which players could join the grand coalition one by one. For each ordering, player $i$'s marginal contribution is the value added when $i$ joins. The Shapley value is the average of these marginal contributions over all $n!$ permutations.

The Shapley value provides a principled answer to a fundamental question: when a group of agents cooperate and produce a joint surplus, how should that surplus be divided so that each agent receives a share proportional to what they genuinely contribute?

## Historical Context

Lloyd Shapley introduced the value in his 1953 paper "A Value for n-Person Games," published in *Contributions to the Theory of Games II* (Annals of Mathematics Studies, vol. 28). The work emerged from Shapley's doctoral thesis at Princeton under Albert Tucker. Shapley proved that his value is the **unique** allocation rule satisfying four axioms (see Key Properties below), establishing it as a canonical fairness criterion.

The concept rapidly became one of the most influential ideas in game theory. In 1988, Alvin Roth edited *The Shapley Value: Essays in Honor of Lloyd S. Shapley*, and in 2020, a *Handbook of the Shapley Value* was published for the concept's 65th anniversary.

In 2012, Lloyd Shapley and Alvin Roth were awarded the **Nobel Memorial Prize in Economic Sciences** "for the theory of stable allocations and the practice of market design," recognizing Shapley's foundational contributions to cooperative game theory and matching theory.

## Key Properties: The Four Axioms

The Shapley value is the unique allocation rule satisfying these four axioms simultaneously:

- **Efficiency (Pareto optimality)**: The total payoff distributed equals the value of the grand coalition: $\sum_{i \in N} \phi_i(v) = v(N)$. Nothing is wasted and nothing is left undistributed.
- **Symmetry**: If players $i$ and $j$ make identical marginal contributions to every coalition ($v(S \cup \{i\}) = v(S \cup \{j\})$ for all $S \subseteq N \setminus \{i, j\}$), then $\phi_i(v) = \phi_j(v)$. Interchangeable players receive equal shares.
- **Dummy player (null player)**: If player $i$ adds only their standalone value to every coalition ($v(S \cup \{i\}) - v(S) = v(\{i\})$ for all $S$), then $\phi_i(v) = v(\{i\})$. Players who contribute nothing beyond their solo value receive exactly that solo value.
- **Additivity (linearity)**: For two games $v$ and $w$ on the same player set, $\phi_i(v + w) = \phi_i(v) + \phi_i(w)$. This allows decomposition of complex games into simpler components.

**Uniqueness theorem**: Shapley (1953) proved that these four axioms uniquely determine the value. No other allocation rule satisfies all four simultaneously. This axiomatic uniqueness is the primary reason the Shapley value is considered the gold standard for fair division in cooperative settings.

## Taxonomy: Extensions and Variants

| Variant | Author(s) / Year | Key Modification | Domain |
|---------|-------------------|------------------|--------|
| **Shapley value** (original) | Shapley, 1953 | Average marginal contribution over all permutations | Cooperative games |
| **Myerson value** | Myerson, 1977 | Restricts cooperation to connected subgraphs in a communication network | Network/graph games |
| **Banzhaf power index** | Banzhaf, 1965 | Weights all coalitions equally (not all permutations); does not satisfy efficiency | Voting games |
| **Owen value** | Owen, 1977 | Extends Shapley to games with a priori unions (coalition structure) | Games with coalition structure |
| **Weighted Shapley value** | Shapley, 1953; Kalai & Samet, 1987 | Assigns different weights to players reflecting asymmetric importance | Asymmetric games |
| **SHAP values** | Lundberg & Lee, 2017 | Applies Shapley framework to ML feature attribution; features as "players" | ML interpretability |

### The Myerson Value (1977)

Roger Myerson extended the Shapley value to **graph-restricted games** where players can only cooperate if they are connected in a communication network. Given a graph $G = (N, E)$ on the player set, the Myerson value computes the Shapley value of a *restricted game* $v^G$ in which the worth of any coalition $S$ equals the sum of worths of its connected components in $G$:

$$v^G(S) = \sum_{C \in S/G} v(C)$$

The Myerson value is the unique allocation rule on communication games satisfying **component efficiency** (each connected component distributes exactly its own value) and **fairness** (removing a link between $i$ and $j$ changes both their payoffs by the same amount). This extension is foundational to **network game theory**, where the structure of relationships constrains who can cooperate with whom.

## Notable Systems and Implementations

| System / Method | Mechanism | Application |
|----------------|-----------|-------------|
| **SHAP** (Lundberg & Lee, 2017) | Treats ML features as players; prediction as coalition value; computes Shapley values for feature attribution | Model-agnostic ML interpretability |
| **KernelSHAP** | Weighted linear regression to approximate SHAP values | Arbitrary ML models |
| **TreeSHAP** (Lundberg et al., 2019) | Polynomial-time exact SHAP for tree-based models exploiting tree structure | XGBoost, Random Forests, LightGBM |
| **Shapley-Shubik index** (1954) | Shapley value applied to simple (voting) games | Measuring voting power in legislatures and committees |
| **Aumann-Shapley pricing** | Continuous extension for cost allocation in production economies | Utility pricing, telecommunications |

## Applications

| Domain | Application | How Shapley Value Is Used |
|--------|------------|--------------------------|
| **ML interpretability** | Feature importance (SHAP) | Each feature is a "player"; the prediction is the coalition value; Shapley values quantify each feature's contribution to a specific prediction |
| **Voting power** | Shapley-Shubik power index | Measures a voter's probability of being the pivotal (swing) voter across all possible orderings |
| **Cost sharing** | Airport cost allocation, infrastructure | Distributes shared costs among users proportionally to their marginal impact on total cost |
| **Network analysis** | Centrality and influence | Shapley-based centrality measures quantify a node's contribution to network connectivity or information flow |
| **Economics** | Fair division, market design | Determines fair payoffs in joint ventures, patent pools, and supply chain coalitions |
| **Telecommunications** | Network pricing | Allocates costs of shared infrastructure among service providers |

## Computational Complexity

Computing the exact Shapley value is computationally expensive:

- **General case**: Computing the Shapley value for arbitrary coalitional games requires evaluating $2^n$ coalitions, making it **#P-complete** (which subsumes NP-hardness). For weighted voting games specifically, exact computation is #P-hard.
- **Polynomial special cases**: For certain structured game classes, efficient computation is possible:
  - **Unanimity games**: Closed-form solution
  - **Superadditive games with special structure**: e.g., convex games, assignment games
  - **Tree-structured games**: The Myerson value on trees can be computed in polynomial time
  - **TreeSHAP**: Exact SHAP values for tree-based ML models in $O(TLD^2)$ time (T = trees, L = leaves, D = depth)
- **Approximation**: Monte Carlo sampling of random permutations provides unbiased estimates with convergence guarantees. This is the dominant approach in practice (e.g., KernelSHAP).

## Challenges and Limitations

- **Exponential complexity**: The $2^n$ coalition evaluation requirement makes exact computation infeasible for large player sets (beyond approximately 25-30 players without special structure)
- **Superadditivity assumption**: The classical framework assumes the grand coalition forms; in practice, stable subcoalitions may be preferred (addressed by the core, nucleolus, and other solution concepts)
- **Sensitivity to value function specification**: Results depend heavily on how the characteristic function $v$ is defined; in SHAP, this translates to the choice of baseline/background distribution
- **Correlation among features**: When ML features are correlated, SHAP values can be misleading because the marginal contribution calculation assumes feature independence in the default KernelSHAP formulation
- **Interpretation challenges**: Shapley values explain individual predictions but do not directly reveal causal mechanisms or global model behavior

## Related Terms

- **[XAI - Explainable AI](term_xai.md)**: SHAP is one of the most widely used XAI methods; the Shapley value provides its axiomatic foundation
- **[GNN - Graph Neural Networks](term_gnn.md)**: GNN-based approaches can leverage Shapley-style attribution for explaining graph predictions; Myerson value connects to graph-structured cooperation
- **[Personalized PageRank (PPR)](term_ppr.md)**: Alternative network centrality measure; both PPR and Shapley-based centrality quantify node importance but from different axiomatic foundations

## References

### Vault Sources

### External Sources
- [Shapley (1953). "A Value for n-Person Games." *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28, pp. 307-317](https://doi.org/10.1515/9781400881970-018) — the foundational paper defining the Shapley value and proving its axiomatic uniqueness
- [Myerson (1977). "Graphs and Cooperation in Games." *Mathematics of Operations Research* 2(3), pp. 225-229](https://doi.org/10.1287/moor.2.3.225) — extends the Shapley value to graph-restricted (network) games
- [Lundberg & Lee (2017). "A Unified Approach to Interpreting Model Predictions." *NeurIPS 2017*](https://arxiv.org/abs/1705.07874) — introduces SHAP, connecting Shapley values to ML feature importance
- [Roth (1988). *The Shapley Value: Essays in Honor of Lloyd S. Shapley.* Cambridge University Press](https://doi.org/10.1017/CBO9780511528446) — comprehensive collection of extensions and applications
- [Christoph Molnar. "Interpretable Machine Learning" — Ch. 17: Shapley Values](https://christophm.github.io/interpretable-ml-book/shapley.html) — accessible explanation of Shapley values for ML practitioners
- [Wikipedia: Shapley Value](https://en.wikipedia.org/wiki/Shapley_value)
- [RAND Corporation (2016). "Lloyd S. Shapley, Nobel Laureate in Economics, Dies at 92"](https://www.rand.org/news/press/2016/03/14.html) — biographical context and Nobel Prize recognition
