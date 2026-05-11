---
tags:
  - resource
  - terminology
  - quantization
  - nearest_neighbor
  - vector_search
  - compression
keywords:
  - Product Quantization
  - PQ
  - subspace quantization
  - codebook
  - k-means
  - IVF-PQ
  - FAISS
  - ANN search
  - vector compression
topics:
  - Vector Quantization
  - Approximate Nearest Neighbor Search
  - Data Compression
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# Product Quantization (PQ)

## Definition

**Product Quantization (PQ)** is a vector compression technique (Jégou et al., 2011) that enables efficient approximate nearest neighbor search by decomposing high-dimensional vectors into subvectors and quantizing each subvector independently with its own small codebook. A D-dimensional vector is split into $M$ subvectors of dimension $D/M$, each quantized to one of $K$ centroids learned via k-means — producing a compact code of $M \cdot \lceil\log_2 K \rceil$ bits.

PQ's key advantage is that distance computation between a query and compressed database vectors can be performed via **lookup table** operations: pre-compute distances from the query's subvectors to all $K$ centroids in each subspace, then sum $M$ table lookups per database vector. This achieves $O(M)$ distance computation instead of $O(D)$, combined with dramatic memory reduction ($M \cdot 8$ bits typical vs $4D$ bytes for float32).

PQ is the **dominant compression method for billion-scale ANN search** and the foundation of FAISS's IVF-PQ index.

## Key Properties

- **Subspace decomposition**: Splits D-dim space into M independent subspaces — avoids exponential codebook size of full VQ
- **Data-dependent codebooks**: Each subspace's codebook is learned via k-means on training data — captures data distribution
- **Asymmetric Distance Computation (ADC)**: Query is not quantized; distances computed between exact query subvectors and codebook entries
- **Lookup table speedup**: Pre-compute M × K distance table → each database vector requires only M table lookups
- **Memory efficient**: Typical 8 bits per subspace × M subspaces = 8M bytes vs 4D bytes for float32
- **IVF-PQ**: Combined with Inverted File Index for coarse-to-fine search — the production standard in FAISS
- **Limitations**: Data-dependent (requires k-means training); no theoretical error bounds (unlike RaBitQ); can fail catastrophically on some datasets

## Comparison with Other Methods

| Aspect | PQ | RaBitQ | TurboQuant | LSH |
|--------|-----|--------|------------|-----|
| **Data-dependent** | Yes (k-means) | No (random rotation) | No (random rotation) | No (random hash) |
| **Error bounds** | None | O(1/√D) | ~2.7× optimal | Probabilistic |
| **Bits per vector** | ~64-128 | D | Variable | D × L |
| **Distance computation** | Lookup table | Bitwise XOR | Scalar ops | Hamming |
| **Failure risk** | Catastrophic on some data | None (uniform) | None (uniform) | None (uniform) |

## Related Terms

- **[Vector Quantization](term_vector_quantization.md)**: PQ is the most widely-used VQ variant; decomposes the full VQ problem into independent subspace quantizations
- **[IVF](term_ivf.md)**: Inverted File Index; coarse partitioning often combined with PQ (IVF-PQ) for scalable ANN search
- **[ANN Search](term_ann_search.md)**: PQ is one of four major ANN method families (quantization-based)
- **[RaBitQ](term_rabitq.md)**: Data-oblivious alternative to PQ with formal error bounds; outperforms PQ with half the bits
- **[TurboQuant](term_turboquant.md)**: Extends rotation-based quantization to multi-bit; shares near-optimal guarantees that PQ lacks
- **[FAISS](term_faiss.md)**: Facebook's ANN library; IVF-PQ is its primary production index
- **[LSH](term_lsh.md)**: Hash-based ANN alternative; data-oblivious like RaBitQ/TurboQuant but produces hash buckets, not distance estimates
- **[KNN](term_knn.md)**: Exact KNN is what PQ-based ANN approximates
- **[HNSW](term_hnsw.md)**: Graph-based ANN alternative; often combined with PQ for memory efficiency

## References

### External Sources

- [Jégou, H., Douze, M., & Schmid, C. (2011). "Product Quantization for Nearest Neighbor Search." IEEE TPAMI](https://ieeexplore.ieee.org/document/5432202) — Original PQ paper
- [Wikipedia: Vector Quantization](https://en.wikipedia.org/wiki/Vector_quantization) — VQ overview including PQ
- [FAISS Wiki: Product Quantization](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) — Implementation details
