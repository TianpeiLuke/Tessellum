---
tags:
  - resource
  - terminology
  - network_science
  - statistical_inference
  - random_graph_theory
  - social_network_analysis
keywords:
  - exponential random graph model
  - ERGM
  - p-star model
  - p* model
  - exponential family
  - sufficient statistics
  - MCMC estimation
  - network statistics
  - model degeneracy
  - curved ERGM
  - GWESP
  - geometrically weighted
topics:
  - Statistical Network Analysis
  - Random Graph Theory
  - Social Network Analysis
  - Statistical Inference on Networks
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Exponential Random Graph Model (ERGM / p* Model)

## Definition

An **Exponential Random Graph Model (ERGM)**, also known as the **p* model**, is a statistical model for network data that expresses the probability of observing a particular graph $G$ as an exponential function of a vector of network statistics. The general form is:

$$P_\theta(G) = \frac{1}{\kappa(\theta)} \exp\!\bigl(\theta^\top s(G)\bigr)$$

where $\theta$ is a vector of parameters, $s(G)$ is a vector of **sufficient statistics** computed from the graph (e.g., edge count, triangle count, $k$-star count, homophily terms), and $\kappa(\theta) = \sum_{G'} \exp(\theta^\top s(G'))$ is the normalizing constant summing over all possible graphs on the same vertex set. This normalizing constant is generally intractable for even moderate-sized networks, since the number of possible graphs on $n$ nodes scales as $2^{\binom{n}{2}}$.

ERGMs belong to the **exponential family** of distributions, which means they inherit key statistical properties: the sufficient statistics $s(G)$ capture all the information in the data relevant to the parameters $\theta$, and maximum likelihood estimation has well-understood asymptotic properties (when it can be computed). The framework provides a principled way to test competing hypotheses about the structural forces that shape a network -- for instance, whether an observed network's clustering is better explained by transitivity, homophily, or both -- by including the corresponding statistics in a single model and testing their effects against each other.

## Historical Context

| Period | Figure(s) | Contribution |
|--------|-----------|-------------|
| 1981 | **Holland, Leinhardt** | Introduced the **p1 model** for directed networks with dyadic independence, an early parametric model for social networks |
| 1986 | **Frank, Strauss** | Proposed **Markov random graphs**, introducing dependence between edges that share a node; established the exponential family form using results from spatial statistics (Besag 1974) |
| 1996 | **Wasserman, Pattison** | Generalized Frank-Strauss to the **p* model** with more complex dependence structures, incorporated node attributes (covariates), and distinguished social selection from social influence |
| 2003 | **Handcock** | Characterized the **degeneracy problem** in Markov graph ERGMs, showing that standard triangle and $k$-star statistics produce near-degenerate distributions |
| 2006 | **Snijders, Pattison, Robins, Handcock** | Introduced **new specifications** with alternating $k$-stars and alternating $k$-triangles as curved exponential family terms, largely resolving the degeneracy problem |
| 2007 | **Robins, Pattison, Kalish, Lusher** | Published an influential introduction and overview of modern ERGM methodology, consolidating theoretical advances and practical estimation guidance |
| 2008 | **Hunter, Handcock, Butts, Goodreau, Morris** | Released the **ergm** R package (statnet suite), providing the standard software implementation with MCMC-MLE estimation and goodness-of-fit diagnostics |

## Taxonomy

### Sufficient Statistics Commonly Used in ERGMs

| Statistic | What It Captures | Notes |
|-----------|-----------------|-------|
| **Edge count** | Baseline tie density | ERGM with only this term is equivalent to $G(n,p)$ Erdos-Renyi model |
| **$k$-stars** ($S_k$) | Degree heterogeneity | Count of nodes with $k$ or more ties; prone to degeneracy in Markov ERGMs |
| **Triangle count** | Transitivity / clustering | Captures "friend of a friend" closure; standard count is degenerate for large networks |
| **GWESP** (Geometrically Weighted Edgewise Shared Partners) | Transitivity with diminishing returns | Curved ERGM term; down-weights additional shared partners geometrically; resolves triangle degeneracy |
| **GWD** (Geometrically Weighted Degree) | Degree distribution shape | Curved term for degree heterogeneity; replaces $k$-star counts |
| **Homophily terms** (`nodematch`, `absdiff`) | Attribute-based [assortative mixing](term_assortative_mixing.md) | Measures tendency for nodes with similar attributes to form ties |
| **Reciprocity** (`mutual`) | Mutual tie formation in directed networks | Captures whether directed ties tend to be reciprocated |
| **Nodal covariates** (`nodecov`, `nodeicov`) | Attribute effects on degree | Models whether a node attribute increases or decreases tie propensity |

### ERGM Variants

| Variant | Key Feature |
|---------|-------------|
| **Bernoulli / dyad-independent ERGM** | No dependence between edges; equivalent to logistic regression on dyads |
| **Markov ERGM** (Frank-Strauss) | Edges sharing a node are dependent; uses triangle and $k$-star counts |
| **Curved ERGM** | Nonlinear parameter-statistic mapping; uses geometrically weighted terms (GWESP, GWD) |
| **Social circuit ERGM** | Dependence based on 4-cycles rather than triangles; alternative to Markov specification |
| **Valued ERGM** | Extends to weighted networks with continuous or count-valued edges |
| **Temporal ERGM (TERGM)** | Models network evolution over discrete time steps |

## Key Properties

- **Exponential family membership**: ERGMs inherit the statistical properties of exponential families -- existence of sufficient statistics, convexity of the log-partition function, and conjugate prior structure for Bayesian inference
- **Erdos-Renyi as special case**: An ERGM with only the edge count statistic $s(G) = |E|$ reduces to the $G(n,p)$ model with $p = \text{logistic}(\theta)$; all richer ERGMs can be understood as departures from this baseline
- **MCMC-based estimation**: Because the normalizing constant $\kappa(\theta)$ is intractable, maximum likelihood estimation requires Markov Chain Monte Carlo methods -- specifically, MCMC-MLE uses simulated networks to approximate the likelihood ratio at each iteration (Geyer-Thompson approach)
- **Model degeneracy**: Naive Markov ERGM specifications (using raw triangle and $k$-star counts) tend to place nearly all probability mass on either empty or complete graphs, with negligible probability on realistic intermediate networks; this is the **degeneracy problem** identified by Handcock (2003)
- **Curved ERGM resolution**: Geometrically weighted statistics (GWESP, GWD) introduced by Snijders et al. (2006) and Hunter (2007) largely resolve degeneracy by imposing diminishing marginal effects -- the $k$-th additional shared partner contributes geometrically less than the $(k-1)$-th
- **Goodness-of-fit assessment**: Model adequacy is evaluated by simulating networks from the fitted ERGM and comparing structural statistics (degree distribution, geodesic distance distribution, edgewise shared partner distribution) between simulated and observed networks
- **Interpretable parameters**: Each parameter $\theta_i$ has a log-odds interpretation -- it represents the change in the conditional log-odds of a tie for a unit change in the corresponding statistic $s_i(G)$, holding other statistics constant
- **Computational cost**: MCMC estimation scales poorly with network size; practical applications are typically limited to networks of a few thousand nodes, though recent advances in snowball sampling and parallel MCMC have extended this range

## Applications

| Domain | Application | ERGM Role |
|--------|------------|-----------|
| **Social network analysis** | Testing theories of tie formation (homophily, reciprocity, transitivity) | Model competing structural hypotheses in a unified statistical framework |
| **Organizational studies** | Analyzing advice-seeking, collaboration, or communication networks | Estimate effects of hierarchy, departmental structure, and individual attributes on tie formation |
| **Public health** | Modeling disease transmission networks | Capture network features (clustering, degree heterogeneity) that affect epidemic dynamics |
| **Political science** | Studying co-sponsorship, alliance, or trade networks | Test whether ties form due to ideological similarity, geographic proximity, or structural balance |
| **Ecology** | Food webs and species interaction networks | Model predator-prey or mutualistic relationships with node-level traits (body size, trophic level) |

## Challenges and Limitations

- **Degeneracy**: Standard Markov ERGM specifications are prone to near-degenerate distributions; curved ERGMs mitigate but do not entirely eliminate this issue, and modelers must carefully check MCMC diagnostics
- **Scalability**: MCMC estimation is computationally expensive, limiting practical application to networks of moderate size (typically $n < 5000$); larger networks require approximate methods or model simplification
- **Model selection**: Choosing which statistics to include requires substantive theory and iterative goodness-of-fit checking; there is no automated procedure that reliably identifies the best specification
- **Cross-sectional limitation**: Standard ERGMs model a single observed network snapshot; they cannot directly distinguish between the social processes that generated the network and require longitudinal extensions (TERGM, SAOM) for causal interpretation
- **Convergence diagnostics**: MCMC chains may fail to converge or mix poorly, particularly for models near the degeneracy boundary; careful monitoring of trace plots and Geweke diagnostics is essential

## Related Terms

- **[Random Graph (Erdos-Renyi)](term_random_graph.md)**: ERGM with only an edge count statistic is mathematically equivalent to the $G(n,p)$ model; the ER model is the simplest possible ERGM
- **[Configuration Model](term_configuration_model.md)**: A null model that preserves the degree sequence while randomizing other structure; provides a complementary baseline to ERGMs for assessing network properties
- **[Stochastic Block Model](term_stochastic_block_model.md)**: Can be formulated as a special case of ERGM with block-membership-dependent edge probabilities; both are generative models for network data but SBMs emphasize community structure
- **[Homophily](term_homophily.md)**: A key social process modeled in ERGMs via `nodematch` and `absdiff` statistics that capture the tendency for similar nodes to form ties
- **[Community Detection](term_community_detection.md)**: ERGMs can model community structure through block-level covariates or mixing terms; ERGM-based approaches provide a statistical inference alternative to algorithmic community detection
- **[Small-World Network](term_small_world_network.md)**: The triangle and clustering statistics central to ERGMs directly measure the local clustering that defines small-world structure; ERGMs can test whether observed clustering exceeds random baseline expectations

- **[Exponential Family](term_exponential_family.md)**: ERGMs are exponential family models for network data

## References

### Vault Sources

### External Sources
- [Frank, O. & Strauss, D. (1986). "Markov Graphs." *Journal of the American Statistical Association*, 81(395), 832-842](https://doi.org/10.1080/01621459.1986.10478342) — introduced Markov dependence assumptions and the exponential family form for random graphs
- [Wasserman, S. & Pattison, P. (1996). "Logit Models and Logistic Regressions for Social Networks: I. An Introduction to Markov Graphs and p*." *Psychometrika*, 61(3), 401-425](https://doi.org/10.1007/BF02294547) — generalized Frank-Strauss to the p* framework with node attributes and flexible dependence structures
- [Snijders, T.A.B., Pattison, P.E., Robins, G.L. & Handcock, M.S. (2006). "New Specifications for Exponential Random Graph Models." *Sociological Methodology*, 36(1), 99-153](https://doi.org/10.1111/j.1467-9531.2006.00176.x) — introduced alternating statistics and curved ERGM specifications that resolve the degeneracy problem
- [Robins, G., Pattison, P., Kalish, Y. & Lusher, D. (2007). "An Introduction to Exponential Random Graph (p*) Models for Social Networks." *Social Networks*, 29(2), 173-191](https://doi.org/10.1016/j.socnet.2006.08.002) — accessible overview of modern ERGM theory and methodology
- [Hunter, D.R., Handcock, M.S., Butts, C.T., Goodreau, S.M. & Morris, M. (2008). "ergm: A Package to Fit, Simulate and Diagnose Exponential-Family Models for Networks." *Journal of Statistical Software*, 24(3)](https://doi.org/10.18637/jss.v024.i03) — reference paper for the statnet/ergm R package implementing MCMC-MLE estimation
- [Jackson, M.O. (2008). *Social and Economic Networks*. Princeton University Press, Ch. 3, Ch. 13](https://press.princeton.edu/books/hardcover/9780691134406/social-and-economic-networks) — textbook treatment of ERGMs in the context of strategic network formation and statistical network models
