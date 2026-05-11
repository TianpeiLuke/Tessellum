---
tags:
  - resource
  - terminology
  - graph_algorithms
  - retrieval
  - ranking
keywords:
  - PageRank
  - link analysis
  - power iteration
  - damping factor
  - teleportation
  - personalized PageRank
  - global importance
topics:
  - Graph Algorithms
  - Information Retrieval
  - Web Search
language: markdown
date of note: 2026-04-28
status: active
building_block: concept
---

# PageRank

## Definition

**PageRank** is a graph-based importance algorithm that assigns each node a score equal to the long-run probability that a random walker — following outgoing edges with probability *α* and uniformly teleporting elsewhere with probability (1 − α) — visits it. Originally developed at **Stanford in 1996 by Larry Page and Sergey Brin** as the differentiating ranking algorithm of what became Google, PageRank is the basis of a family of variants: **standard PageRank** (uniform teleportation → global importance), **Personalized PageRank / PPR** (teleportation concentrated on seeds → topic-relative importance, Haveliwala 2002), **Topic-Sensitive PageRank** (teleportation over a topic-relevant subset), **Intelligent Surfer** (query-dependent variant, Richardson & Domingos 2001), and **TrustRank** (anti-spam variant). The algorithm was patented by Stanford (granted 2001, now expired) and exclusively licensed to Google for 1.8 million shares of stock.

Mathematically, PageRank is the **dominant right eigenvector of the modified adjacency matrix** (link matrix combined with the random-jump component, columns rescaled to sum to one) — i.e., it is an instance of **eigenvector centrality**. Computed in practice via **power iteration** on the row-normalized adjacency matrix until the score vector converges (typically tens of iterations for web-scale and vault-scale graphs).

## Mathematical Formulation

The PageRank score of node $v$ is defined recursively as

$$\text{PR}(v) = \frac{1 - \alpha}{N} + \alpha \sum_{u \in B(v)} \frac{\text{PR}(u)}{L(u)}$$

where $N$ is the total number of nodes, $B(v)$ is the set of nodes pointing to $v$, $L(u)$ is the out-degree of $u$, and $\alpha$ is the damping factor (conventionally $\alpha = 0.85$).

In matrix form, with $M$ the column-stochastic transition matrix and $\mathbf{1}$ the all-ones vector,

$$\hat{M} = \alpha M + \frac{1 - \alpha}{N} \mathbf{1} \mathbf{1}^{\top}, \qquad \mathbf{x} = \hat{M}\, \mathbf{x}$$

The unique stationary score vector $\mathbf{x}$ is computed by **power iteration**

$$\mathbf{x}^{(t+1)} = \hat{M}\, \mathbf{x}^{(t)}$$

until $\|\mathbf{x}^{(t+1)} - \mathbf{x}^{(t)}\|_1 < \varepsilon$. Convergence rate is governed by the second-largest eigenvalue $|\lambda_2| \le \alpha$ of $\hat{M}$. The **personalized** variant replaces the uniform jump distribution $\tfrac{1}{N}\mathbf{1}$ with a sparse personalization vector $\mathbf{d}$ concentrated on the seed set.

## Context

In the SlipBox, PageRank appears in two roles:

1. **Static (global) PageRank** — `scripts/ppr.py:static_pagerank()` precomputes the score for every note offline; results are stored in the `notes.static_ppr_score` column and used as a tie-breaker / minor weight in keyword ranking. Following FZ 5j1a1a1 evidence that `in_degree ≈ static_ppr_score`, the production builder swapped expensive NetworkX PageRank for a SQL `COUNT(*)` aggregate at index time.
2. **Query-time Personalized PageRank** — `scripts/ppr.py:query_pagerank()` builds a personalization vector concentrated on query-relevant seed notes and runs `networkx.pagerank(G, alpha, personalization)`. Wrapped by `scripts/ppr_search.py` (Strategy 7 in `slipbox-search-notes`).

## Key Characteristics

- **Damping factor α (default 0.85)** controls the trade-off between graph-following (α) and teleportation (1 − α). Lower α keeps more mass near the teleportation set; higher α spreads mass further across the graph. The 0.85 value is the conventional default from the original Brin & Page paper, interpreted as the probability the "random surfer" continues clicking links rather than jumping to a new page.
- **Teleportation distribution** is the only difference between PageRank variants. Uniform-over-all-nodes → standard; concentrated on a seed set → personalized; weighted by topic priors → topic-sensitive.
- **Power iteration converges fast** in practice — convergence rate is governed by the spectral gap of the transition matrix; teleportation guarantees the walk is irreducible and aperiodic, so the stationary distribution exists and is unique.
- **Hub bias is real.** High-in-degree nodes attract high PageRank. In knowledge graphs this means term-dictionary cards / entry-points sit at the top of static PageRank, which is *not* the same as topical relevance — the basis for the SlipBox's "never use static PPR alone for content retrieval" rule and the FZ 5j1 finding that PageRank ≈ in-degree on this corpus.
- **Beyond the web**, PageRank is now applied to academic citation analysis, protein-interaction networks, ecological-importance scoring of species, neuron firing-rate inference, sports rankings, and social-network influence modeling — wherever a directed network has nodes whose importance is determined by their incoming connections.

## Related Terms

- **[PPR](term_ppr.md)** — Personalized variant; the production retrieval algorithm in this vault
- **[Random Walk](term_random_walk.md)** — the underlying stochastic process PageRank computes the stationary distribution of
- **[Eigenvector Centrality](term_eigenvector_centrality.md)** — PageRank IS the eigenvector centrality of the row-stochastic transition matrix with damping
- **[Network Centrality](term_network_centrality.md)** — broader family; PageRank is one of the dominant centrality measures
- **[Spectral Graph Theory](term_spectral_graph_theory.md)** — spectral perspective on PageRank; convergence rate set by the spectral gap
- **[Adjacency Matrix](term_adjacency_matrix.md)** — the matrix PageRank operates on; row-normalized to make a stochastic transition matrix
- **[Information Retrieval](term_information_retrieval.md)** — PageRank's original IR application (web search) and the field that consumes it for document ranking
- **[GNN](term_gnn.md)** — Graph Neural Networks generalize the message-passing pattern that diffusion-based PageRank uses
- **[Embedding](term_embedding.md)** — content-based ranking signal; complementary to graph-based PageRank
- **[Bayesian Learning on Networks](term_bayesian_learning_on_networks.md)** — adjacent: PageRank as a uniform prior over node importance, Bayesian posteriors as topic-sensitive variants

## References

- [Brin & Page, "The Anatomy of a Large-Scale Hypertextual Web Search Engine" (1998)](http://infolab.stanford.edu/~backrub/google.html) — original PageRank paper
- [Page, Brin, Motwani & Winograd, "The PageRank Citation Ranking: Bringing Order to the Web" (1999)](http://ilpubs.stanford.edu:8090/422/) — technical report with full math + power-iteration derivation
- [Haveliwala, "Topic-Sensitive PageRank" (WWW 2002)](http://ilpubs.stanford.edu:8090/506/) — personalized / topic-sensitive variant
- [Richardson & Domingos, "The Intelligent Surfer" (NIPS 2001)](https://homes.cs.washington.edu/~pedrod/papers/nips01.pdf) — query-dependent PageRank
- [NetworkX `pagerank` API](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html) — implementation used by the SlipBox
- [Wikipedia — PageRank](https://en.wikipedia.org/wiki/PageRank)
