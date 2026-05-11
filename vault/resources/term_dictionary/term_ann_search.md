---
tags:
  - resource
  - terminology
  - nearest_neighbor
  - similarity_search
  - vector_database
  - algorithms
keywords:
  - ANN
  - approximate nearest neighbor
  - similarity search
  - vector search
  - HNSW
  - IVF
  - vector database
  - high-dimensional search
  - kNN
topics:
  - Similarity Search
  - Vector Databases
  - Algorithms
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# ANN (Approximate Nearest Neighbor) Search

## Definition

**Approximate Nearest Neighbor (ANN) search** is the problem of finding points in a dataset that are close to a query point in high-dimensional space, with the relaxation that the returned neighbors need only be approximately closest rather than exactly closest. This relaxation enables algorithms that scale **sublinearly** in dataset size — essential for billion-scale vector databases where exact nearest neighbor search (brute-force $O(nd)$) is prohibitively expensive.

Formally, a $(c, r)$-approximate nearest neighbor algorithm returns a point within distance $cr$ of the query whenever a true nearest neighbor exists within distance $r$, where $c > 1$ is the approximation factor.

## Key Properties

- **Sublinear query time**: ANN algorithms achieve $O(n^\rho)$ or $O(\log n)$ query time vs $O(n)$ brute-force, where $\rho < 1$
- **Accuracy-speed tradeoff**: More index structure → faster queries but higher memory and potential accuracy loss
- **Curse of dimensionality**: Exact NN degrades to brute-force in high dimensions; ANN methods circumvent this via approximation
- **Distance metrics**: Euclidean ($\ell_2$), cosine similarity, inner product, Hamming distance
- **Index types**: Graph-based (HNSW), partition-based (IVF), hash-based (LSH), quantization-based (PQ, RaBitQ)

## Taxonomy of Methods

| Category | Method | Mechanism | Strengths |
|----------|--------|-----------|-----------|
| **Graph-based** | HNSW | Navigable small world graph with skip-list hierarchy | Best recall-speed tradeoff; dominant in practice |
| **Partition-based** | IVF (Inverted File) | Voronoi partition via k-means; search nearest clusters | Scalable to billions with disk-based variants |
| **Hash-based** | LSH | Locality-sensitive hashing into buckets | Theoretical guarantees; data-oblivious |
| **Quantization-based** | PQ, RaBitQ, TurboQuant | Compress vectors; estimate distances from compressed codes | Memory-efficient; enables in-memory search on large datasets |
| **Tree-based** | KD-tree, Ball tree | Recursive space partitioning | Good for low dimensions; degrades in high-D |
| **Hybrid** | IVF-PQ, IVF-HNSW | Combine partition + quantization or partition + graph | Production standard (FAISS IVF-PQ) |

## Applications

| Domain | Application | Scale |
|--------|-------------|-------|
| **Vector databases** | Pinecone, Weaviate, Milvus, Qdrant | Billions of vectors |
| **RAG** | Retrieval-augmented generation for LLMs | Millions of document chunks |
| **Recommendation** | Embedding-based item/user similarity | Millions-billions of items |
| **Image search** | Visual similarity search | Billions of images |
| **Abuse detection** | Embedding-based fraud pattern matching | Millions of customer embeddings |
| **Genomics** | DNA/protein sequence similarity | Millions of sequences |

## Related Terms

- **[Dimensionality Reduction](term_dimensionality_reduction.md)**: Preprocessing step; reducing vector dimension before ANN indexing improves performance
- **[Information Retrieval](term_information_retrieval.md)**: ANN powers dense retrieval in modern IR systems (DPR, RAG)
- **[LSH](term_lsh.md)**: Hash-based ANN method with theoretical guarantees; sublinear via locality-sensitive buckets
- **[HNSW](term_hnsw.md)**: Hierarchical Navigable Small World — graph-based ANN; best recall-speed tradeoff in practice
- **[IVF](term_ivf.md)**: Inverted File Index — partition-based ANN via Voronoi cells + fine-grained search
- **[Product Quantization](term_product_quantization.md)**: PQ is the dominant compression method for ANN; IVF-PQ is the production standard
- **[Vector Quantization](term_vector_quantization.md)**: Quantization-based ANN via compressed distance estimation (PQ, RaBitQ)
- **[RaBitQ](term_rabitq.md)**: Randomized VQ for ANN with sharp O(1/√D) error bounds
- **[TurboQuant](term_turboquant.md)**: Near-optimal VQ extending RaBitQ to multi-bit settings and KV caches
- **[KNN](term_knn.md)**: Exact K-nearest neighbors — the problem ANN approximates for efficiency
- **[FAISS](term_faiss.md)**: Facebook's ANN library implementing IVF, PQ, HNSW, and LSH
- **[Vector Database](term_vector_database.md)**: Production systems (Pinecone, Milvus, Qdrant) built on ANN indices
- **[Johnson-Lindenstrauss Lemma](term_johnson_lindenstrauss_lemma.md)**: Theoretical foundation for random projection-based ANN
- **[DPR](term_dpr.md)**: Dense Passage Retrieval produces embeddings that ANN indices serve at scale
- **[HippoRAG](term_hipporag.md)**: RAG system combining knowledge graph traversal with ANN retrieval
- **[PPR](term_ppr.md)**: Personalized PageRank — graph-based relevance scoring; complementary to embedding-based ANN
- **[Embedding](term_embedding.md)**: ANN search operates on embedding vectors
- **[RAG](term_rag.md)**: Retrieval-augmented generation uses ANN for document retrieval
- **[GraphRAG](term_graphrag.md)**: Graph-enhanced RAG combining graph traversal with ANN retrieval

## References

### External Sources

- [Indyk, P. & Motwani, R. (1998). "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality." STOC](https://dl.acm.org/doi/10.1145/276698.276876) — Foundational ANN paper (LSH)
- [Malkov, Y. & Yashunin, D. (2020). "Efficient and Robust Approximate Nearest Neighbor Using Hierarchical Navigable Small World Graphs." IEEE TPAMI](https://arxiv.org/abs/1603.09320) — HNSW
- [ann-benchmarks.com](https://ann-benchmarks.com/) — Standard ANN benchmark comparing methods
