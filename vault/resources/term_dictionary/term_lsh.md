---
tags:
  - resource
  - terminology
  - hashing
  - nearest_neighbor
  - dimensionality_reduction
  - randomized_algorithms
keywords:
  - LSH
  - locality-sensitive hashing
  - approximate nearest neighbor
  - ANN
  - SimHash
  - MinHash
  - random hyperplane
  - hash family
  - similarity search
  - cosine similarity
topics:
  - Approximate Nearest Neighbor Search
  - Randomized Algorithms
  - Similarity Search
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# LSH (Locality-Sensitive Hashing)

## Definition

**Locality-Sensitive Hashing (LSH)** is a family of randomized hashing techniques where **similar items are mapped to the same hash bucket with high probability**, while dissimilar items are mapped to different buckets. Unlike conventional hash functions that minimize collisions, LSH deliberately maximizes collisions for similar inputs — enabling efficient approximate nearest neighbor (ANN) search in sublinear time.

Formally, a hash family $\mathcal{H}$ is $(r_1, r_2, p_1, p_2)$-sensitive if for any two points $x, y$:
- If $d(x, y) \leq r_1$, then $\Pr[h(x) = h(y)] \geq p_1$
- If $d(x, y) \geq r_2$, then $\Pr[h(x) = h(y)] \leq p_2$

where $r_1 < r_2$ and $p_1 > p_2$. The quality of the hash family is measured by $\rho = \ln p_1 / \ln p_2$.

## Historical Context

| Year | Milestone |
|------|-----------|
| 1998 | **Indyk & Motwani** introduce LSH for ANN search in high dimensions |
| 1999 | **Gionis, Indyk, Motwani** propose practical LSH for Hamming distance |
| 2002 | **Charikar** introduces SimHash for cosine similarity (random hyperplane LSH) |
| 2004 | **Broder et al.** formalize MinHash for Jaccard similarity |
| 2015 | **Andoni & Razenshteyn** achieve optimal $\rho$ for Euclidean LSH via cross-polytope |

## Taxonomy

| Hash Family | Distance Metric | Mechanism |
|-------------|----------------|-----------|
| **Random Hyperplane (SimHash)** | Cosine similarity | Random hyperplane partitions; sign of $\langle x, r \rangle$ |
| **MinHash** | Jaccard similarity | Minimum value under random permutation |
| **Bit Sampling** | Hamming distance | Random coordinate selection |
| **Cross-Polytope** | Euclidean distance | Projection onto random cross-polytope vertices |
| **p-Stable (Datar et al.)** | $\ell_p$ distance | Projection + bucketing with p-stable distributions |

## Key Properties

- **Sublinear query time**: $O(n^\rho)$ instead of $O(n)$ brute-force, where $\rho < 1$
- **Probabilistic guarantees**: Finds approximate nearest neighbor with tunable probability via $k$ (hash functions) and $L$ (tables)
- **Data-oblivious**: Hash functions are independent of the data distribution (like [RaBitQ](term_rabitq.md))
- **Composable**: Multiple hash functions can be combined (AND for precision, OR for recall)
- **Streaming-friendly**: Hash values can be computed incrementally as data arrives
- **Trade-off**: More tables $L$ increase recall but also increase memory and query time

## Applications

| Domain | Application |
|--------|-------------|
| **ANN search** | Finding similar items in high-dimensional vector databases |
| **Duplicate detection** | Near-duplicate document/image detection at web scale |
| **Clustering** | Approximate clustering via hash bucket membership |
| **Recommendation** | Finding similar users/items in collaborative filtering |
| **Genomics** | Sequence similarity search in genome databases |
| **Audio fingerprinting** | Shazam-style audio recognition via spectral hashing |

## Related Terms

- **[ANN Search](term_ann_search.md)**: LSH is one of four major ANN method families (alongside graph-based, partition-based, and quantization-based)
- **[RaBitQ](term_rabitq.md)**: Randomized quantization for ANN search; uses similar random rotation technique but produces distance estimates rather than hash buckets
- **[TurboQuant](term_turboquant.md)**: Extends rotation-based quantization to LLM KV caches; shares the random projection paradigm with LSH
- **[Vector Quantization](term_vector_quantization.md)**: Complementary approach — VQ compresses vectors for distance estimation; LSH hashes vectors for bucket-based retrieval
- **[Johnson-Lindenstrauss Lemma](term_johnson_lindenstrauss_lemma.md)**: Theoretical foundation — JL guarantees random projections preserve distances; LSH hash families exploit this
- **[HNSW](term_hnsw.md)**: Graph-based ANN method; often preferred over LSH in practice for better recall-speed tradeoff
- **[KNN](term_knn.md)**: Exact nearest neighbor search; LSH provides approximate KNN in sublinear time
- **[FAISS](term_faiss.md)**: Facebook's vector search library implementing both LSH and VQ-based indices
- **[DPR](term_dpr.md)**: Dense Passage Retrieval uses ANN search (potentially LSH-backed) for document retrieval
- **[PPR](term_ppr.md)**: Personalized PageRank — a different graph-based similarity measure; complementary to LSH's embedding-space approach
- **[Vector Database](term_vector_database.md)**: Production vector databases (Pinecone, Milvus) implement LSH as one indexing strategy
- **[HippoRAG](term_hipporag.md)**: RAG system using vector retrieval — LSH can serve as the underlying index
- **[Quantization](term_quantization.md)**: LSH can be viewed as an extreme quantization (hash → bucket ID)
- **[Embedding](term_embedding.md)**: LSH operates on embedding vectors to enable efficient similarity search

## References

### External Sources

- [Indyk, P. & Motwani, R. (1998). "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality." STOC](https://dl.acm.org/doi/10.1145/276698.276876) — Original LSH paper
- [Charikar, M. (2002). "Similarity Estimation Techniques from Rounding Algorithms." STOC](https://dl.acm.org/doi/10.1145/509907.509965) — SimHash for cosine similarity
- [Wikipedia: Locality-Sensitive Hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) — Comprehensive overview
