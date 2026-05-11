---
tags:
  - resource
  - terminology
  - graph_algorithms
  - probability
  - retrieval
keywords:
  - random walk
  - Markov chain
  - graph traversal
  - stationary distribution
  - teleportation
  - mixing time
topics:
  - Graph Algorithms
  - Probability Theory
  - Knowledge Graph Retrieval
language: markdown
date of note: 2026-04-28
status: active
building_block: concept
---

# Random Walk

## Definition

A **random walk** on a graph is a stochastic process that visits nodes by following edges chosen probabilistically at each step. Starting from one or more *seed* nodes, the walker moves to a neighbor with probability proportional to the edge weight (uniform if unweighted), and either terminates after a fixed number of steps or runs until a **stationary distribution** over nodes is reached. The stationary probability that the walker is at node *v* — the long-run fraction of time spent there — encodes a notion of *graph importance relative to the seeds*: nodes reachable from the seeds via many short paths receive high mass; isolated nodes receive near-zero.

## Mathematical Formulation

For a simple random walk on an undirected unweighted graph $G = (V, E)$ with adjacency $A$ and degree $\deg(v)$, the one-step transition probability from $v$ to neighbor $u$ is:

$$P(X_{t+1} = u \mid X_t = v) = \frac{A_{vu}}{\deg(v)}$$

The **stationary distribution** $\pi$ over nodes is the row vector satisfying

$$\pi = \pi P, \qquad \sum_{v \in V} \pi_v = 1$$

For a connected non-bipartite undirected graph this stationary distribution exists, is unique, and equals $\pi_v = \deg(v) / 2|E|$. Adding a teleportation step with probability $1 - \alpha$ to a fixed distribution $d$ gives the **PageRank-style random walk** whose stationary distribution is the unique solution of

$$\pi^{\top} = \alpha\, P^{\top} \pi^{\top} + (1 - \alpha)\, d^{\top}$$

— the property that makes PageRank well-defined even on disconnected or periodic graphs.

The term was coined by **Karl Pearson in 1905** in a *Nature* letter posing the problem of a wanderer's expected position. The mathematical theory matured under **Pólya's recurrence theorem (1921)**, which proved that a simple random walk almost surely returns to its origin in one and two dimensions but is *transient* (escapes forever with positive probability) in three or more — the source of the popular phrase *"a drunk man will find his way home, but a drunk bird may not."* Random walks are the canonical example of a **discrete-time Markov chain** on a graph.

## Context

Random walks underlie many graph-based retrieval and ranking algorithms in the SlipBox vault: **PageRank** (uniform restart distribution → global importance), **Personalized PageRank / PPR** (restart concentrated on query-relevant seeds → topic-relative importance), **[Pixie](term_pixie_random_walk.md) / DeepWalk / node2vec** (truncated walks producing sequences for embedding training), and **random-walk-with-restart** (closed-form stationary distribution under teleportation). At runtime the SlipBox uses random walks via `scripts/ppr.py` (NetworkX power iteration) on the `note_links` graph, with seeds chosen by query-similarity (`scripts/ppr_search.py`).

Beyond knowledge-graph retrieval, random walks model **Brownian motion** and molecular diffusion in physics, **stock-price dynamics** in the random-walk hypothesis of financial markets, **bacterial chemotaxis** and **genetic drift** in biology, and **web-graph traversal** (PageRank, web-size estimation, image segmentation) in computer science.

## Key Characteristics

- **Seeds determine personalization.** With uniform seeds the walk gives global PageRank; with concentrated seeds it gives topic-sensitive importance (the "personalized" property).
- **Damping factor (α) controls exploration vs locality.** At each step the walker continues along an edge with probability α and "teleports" back to a seed with probability (1 − α). Lower α keeps mass close to seeds (more topical); higher α explores further (more global).
- **Stationary distribution exists and is unique** under mild conditions (irreducibility + aperiodicity), guaranteed by the teleportation step in PageRank-family walks even on disconnected graphs.
- **Convergence is fast in practice.** Power iteration typically converges in tens of iterations on web-scale and vault-scale graphs.
- **Walks are graph-aware where embeddings are not.** Two notes with disjoint vocabulary can score high together if they are graph-neighbors of the same seed — this is the property that makes PPR superior to dense retrieval for multi-hop questions.

## Related Terms

- **[Personalized PageRank](term_ppr.md)** — the random walk with restart personalized to seed nodes; the primary graph-based retrieval algorithm used in GraphRAG and recommendation systems
- **[PPR (GraphRAG)](term_ppr.md)** — Amazon-internal application of Personalized PageRank for knowledge-base graph retrieval in AB Search systems
- **[PageRank](term_pagerank.md)** — the parent algorithm; computes the stationary distribution of a random walk with uniform restart
- **[Eigenvector Centrality](term_eigenvector_centrality.md)** — closely related importance score; PageRank is a damped variant on a row-stochastic matrix
- **[Network Centrality](term_network_centrality.md)** — broader family of node-importance measures, several of which are random-walk-based
- **[Markov Random Field](term_markov_random_field.md)** — adjacent probabilistic model on graphs; random walks are the dynamic counterpart to MRFs' static joint distributions
- **[Belief Propagation](term_belief_propagation.md)** — message-passing alternative to random walks for inference on graph models
- **[Bayesian Learning on Networks](term_bayesian_learning_on_networks.md)** — Bayesian framework where random walks appear as posterior samplers
- **[Complex Contagion](term_complex_contagion.md)** — diffusion process on social/information networks; threshold variant of the random-walk dynamic
- **[Small World Network](term_small_world_network.md)** — graph topology that affects random-walk mixing time
- **[Spectral Graph Theory](term_spectral_graph_theory.md)** — spectral characterization of random-walk transition matrices and convergence rates
- **[Embedding](term_embedding.md)** — alternative content-similarity signal that does NOT use the graph; complementary to random walks
- **[RAG](term_rag.md)** — retrieval-augmented generation; random walks are one retrieval modality used inside RAG pipelines
- **[Pixie Random Walk](term_pixie_random_walk.md)** — Pinterest's production Monte Carlo random-walk-with-restart system; concrete instantiation that approximates PPR via $N$ independent walks instead of matrix iteration

## References

- Pearson, K. (1905). *The Problem of the Random Walk.* Nature, 72(1865), 294 — original use of the term
- Pólya, G. (1921). *Über eine Aufgabe der Wahrscheinlichkeitsrechnung betreffend die Irrfahrt im Strassennetz* — recurrence theorem for 1D / 2D / 3D
- [Lovász, "Random Walks on Graphs: A Survey" (1993)](https://web.cs.elte.hu/~lovasz/erdos.pdf) — comprehensive survey covering mixing time, hitting time, electrical interpretation
- [Wikipedia — Random Walk](https://en.wikipedia.org/wiki/Random_walk)
- [Wikipedia — Random Walks on Graphs](https://en.wikipedia.org/wiki/Random_walks_on_graphs)
