---
tags:
  - resource
  - terminology
  - nearest_neighbor
  - vector_search
  - indexing
keywords:
  - IVF
  - Inverted File Index
  - inverted file
  - Voronoi partition
  - coarse quantizer
  - nprobe
  - IVF-PQ
  - IVF-HNSW
  - FAISS
topics:
  - Approximate Nearest Neighbor Search
  - Vector Indexing
  - Data Structures
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# IVF (Inverted File Index)

## Definition

**Inverted File Index (IVF)** is a partition-based indexing structure for approximate nearest neighbor search that divides the vector space into $C$ Voronoi cells using a coarse quantizer (typically k-means with $C$ centroids), then assigns each database vector to its nearest cell. At query time, only the $\text{nprobe}$ closest cells are searched — reducing the search scope from $N$ vectors to approximately $N \cdot \text{nprobe} / C$.

IVF is rarely used alone — it serves as a **coarse partitioning layer** combined with a fine-grained method:
- **IVF-PQ**: Inverted File + Product Quantization — the production standard for billion-scale search (FAISS)
- **IVF-HNSW**: Inverted File + HNSW graph within each partition
- **IVF-Flat**: Inverted File + exact distance (brute-force within selected cells)

## Key Properties

- **Voronoi partitioning**: k-means creates $C$ cells; each database vector is assigned to its nearest centroid
- **nprobe tradeoff**: More probed cells → higher recall but slower queries; $\text{nprobe} = 1$ is fastest but least accurate
- **Residual coding**: Vectors are stored as residuals from their cell centroid, improving quantization accuracy
- **Scalable**: Handles billions of vectors when combined with PQ compression
- **Data-dependent**: Requires k-means training on representative data
- **Memory**: Cell assignments add minimal overhead; main memory cost is from the fine-grained method (PQ, flat)

## Architecture

```
Query q
    │
    ▼
┌─────────────────────┐
│ Coarse Quantizer    │ ← k-means with C centroids
│ Find nprobe nearest │
│ cells to query      │
└──────────┬──────────┘
           │ nprobe cell IDs
           ▼
┌─────────────────────┐
│ Search within cells │ ← PQ distance / exact / HNSW
│ (only nprobe cells) │
│ N × nprobe/C vectors│
└──────────┬──────────┘
           │
           ▼
     Top-K results
```

## Related Terms

- **[ANN Search](term_ann_search.md)**: IVF is a partition-based ANN method; one of the four major families
- **[Product Quantization](term_product_quantization.md)**: PQ is the standard fine-grained method within IVF cells (IVF-PQ)
- **[HNSW](term_hnsw.md)**: Graph-based ANN; can be used within IVF cells (IVF-HNSW) or as standalone
- **[Vector Quantization](term_vector_quantization.md)**: The coarse quantizer in IVF is itself a form of VQ (k-means)
- **[FAISS](term_faiss.md)**: FAISS's primary production index is IVF-PQ
- **[LSH](term_lsh.md)**: Hash-based partitioning alternative to IVF's k-means partitioning
- **[KNN](term_knn.md)**: IVF-Flat performs exact KNN within selected partitions
- **[Vector Database](term_vector_database.md)**: Production databases (Milvus, Pinecone) use IVF-based indices
- **[Information Retrieval](term_information_retrieval.md)**: IVF borrows the "inverted index" concept from text IR, applied to vector space

## References

### External Sources

- [Jégou, H., Douze, M., & Schmid, C. (2011). "Product Quantization for Nearest Neighbor Search." IEEE TPAMI](https://ieeexplore.ieee.org/document/5432202) — IVF-PQ
- [FAISS Wiki: IVF Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes#cell-probe-methods-indexivf-indexes) — Implementation guide
