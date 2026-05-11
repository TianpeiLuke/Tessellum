---
tags:
  - resource
  - terminology
  - similarity
  - vector_space
  - retrieval
keywords:
  - cosine similarity
  - dot product
  - L2 normalization
  - vector space model
  - dense retrieval
  - angular distance
topics:
  - Vector Space Models
  - Information Retrieval
  - Similarity Metrics
language: markdown
date of note: 2026-04-28
status: active
building_block: concept
---

# Cosine Similarity

## Definition

**Cosine similarity** measures the angular closeness of two vectors as the cosine of the angle between them, computed as the dot product of the vectors divided by the product of their L2 norms:

$$\text{cos}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \, \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^{d} u_i v_i}{\sqrt{\sum_{i=1}^{d} u_i^2} \, \sqrt{\sum_{i=1}^{d} v_i^2}}$$

Range is **[−1, +1]** for arbitrary vectors and **[0, 1]** for non-negative vectors (which is the typical case for embeddings of natural-language content). Crucially, cosine similarity ignores vector *magnitude* — only direction matters — which is desirable for text/embedding retrieval where document length should not bias the ranking. Historically also known as the **Otsuka-Ochiai coefficient** (binary-data variant), the **Tucker coefficient of congruence** (factor-analysis literature), and the **Orchini similarity**.

When both vectors are L2-normalized to unit length ($\|\mathbf{u}\| = \|\mathbf{v}\| = 1$), the formula collapses to a single dot product:

$$\text{cos}(\mathbf{u}, \mathbf{v}) = \mathbf{u} \cdot \mathbf{v}$$

— the algebraic identity that lets dense retrieval pre-normalize the corpus once at index time and reduce query-time scoring to one matrix-vector multiply (no per-query normalization).

The **soft cosine measure** generalizes the formula to take a feature-similarity matrix $S$ rather than treating features as independent:

$$\text{soft\_cos}(\mathbf{u}, \mathbf{v}) = \frac{\sum_{i,j} s_{ij} u_i v_j}{\sqrt{\sum_{i,j} s_{ij} u_i u_j} \, \sqrt{\sum_{i,j} s_{ij} v_i v_j}}$$

— useful when working with synonyms or related terms in vector-space models.

## Context

Cosine similarity is the load-bearing primitive for dense retrieval in the SlipBox. Note embeddings are pre-computed by `scripts/experiments/rag_index_builder.py` using `sentence-transformers/all-MiniLM-L6-v2` and stored as `note_embeddings.npy`; **embeddings are L2-normalized at index time, so cosine similarity reduces to a single matrix-vector dot product** (`scripts/dense_search.py:search()` and `scripts/retrieval_strategies/shared_loaders.py:dense_seed()`). This optimization is what makes Tier-1 dense retrieval fast: no per-query normalization, just `embeddings @ q_emb` followed by `argpartition` for top-k.

## Key Characteristics

- **Magnitude-invariant.** Doubling a vector's length doesn't change its cosine similarity to anything. Important for natural-language content where short and long notes should be comparable.
- **L2-normalized vectors → cosine = dot product.** When both `u` and `v` are unit vectors, `cos(u, v) = u · v`. Pre-normalizing the corpus embeddings collapses cosine retrieval to a single matrix multiply — the key efficiency hack in dense search.
- **Symmetric.** `cos(u, v) = cos(v, u)`. Useful for retrieval (query-vs-doc) and clustering (doc-vs-doc) without code duplication.
- **Geometric, not probabilistic.** Cosine doesn't model word frequency, document length, or smoothing — those concerns belong to BM25 and other lexical scorers. Cosine on dense embeddings captures semantic similarity (paraphrase, hypernymy, related-topic) that BM25 misses.
- **Failure modes.** Identical-direction vectors get cosine 1 even if one carries dramatically different content (rare for trained embeddings but real for tokenized-then-averaged baselines). High cosine ≠ relevance for off-distribution queries.

## Related Terms

- **[Embedding](term_embedding.md)** — the dense vector representations cosine similarity scores
- **[Dense Retrieval](term_dense_retrieval.md)** — the IR family that uses cosine similarity over learned embeddings
- **[Information Retrieval](term_information_retrieval.md)** — broader field where cosine is one of several scoring functions
- **[Attention Mechanism](term_attention_mechanism.md)** — softmax(QK^T / √d) is a normalized similarity score; cosine is the L2-normalized special case
- **[Self-Attention](term_self_attention.md)** — transformer attention computes scaled-dot-product (close cousin of cosine) on token embeddings
- **[Deep Metric Learning](term_deep_metric_learning.md)** — learns embeddings to optimize a chosen similarity/distance metric (often cosine)
- **[Knowledge Distillation](term_knowledge_distillation.md)** — teacher-student methods often use cosine alignment of intermediate representations
- **[FAISS](term_faiss.md)** — Facebook's vector index; scales cosine-similarity search to billions of vectors
- **[PPR](term_ppr.md)** — graph-based ranking that complements cosine retrieval (graph-aware vs content-aware)
- **[Random Walk](term_random_walk.md)** — the alternative graph-traversal-based ranking primitive

## References

- [Manning, Raghavan & Schütze, "Introduction to Information Retrieval", Ch. 6.3 — Dot products and the vector space model](https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html) — canonical IR textbook treatment
- [Sentence-Transformers documentation — semantic textual similarity](https://www.sbert.net/docs/usage/semantic_textual_similarity.html) — the library powering SlipBox dense retrieval
- [Sidorov et al., "Soft Similarity and Soft Cosine Measure" (2014)](https://www.cys.cic.ipn.mx/ojs/index.php/CyS/article/view/2043) — soft cosine extension
- [Wikipedia — Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
