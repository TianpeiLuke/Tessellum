---
tags:
  - resource
  - terminology
  - machine_learning
  - deep_learning
  - representation_learning
keywords:
  - embedding
  - vector representation
  - dense vector
  - word2vec
  - BERT
  - transformer
  - feature representation
  - semantic similarity
topics:
  - machine learning
  - deep learning
  - representation learning
language: markdown
date of note: 2026-02-08
status: active
building_block: concept
---

# Embedding

## Definition

**Embedding** is a learned dense vector representation that maps high-dimensional discrete data (words, entities, items, events) into a continuous, lower-dimensional vector space where semantic similarities are preserved as geometric distances. Embeddings transform behaviors, text, item interactions, and graph relationships into fixed-size numerical vectors that ML models can process. The key insight is that entities with similar characteristics or behaviors cluster together in embedding space, enabling powerful downstream tasks like classification, similarity search, and anomaly detection.

**Key Function**: Convert discrete, high-cardinality data into continuous numerical representations that capture semantic meaning and enable ML models to learn patterns.

## Summary

**Embedding Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Definition** | Dense vector representation mapping discrete data to continuous space |
| **Key Types** | Behavioral, Graph (GNN), Text (BERT), Item/categorical |
| **Typical Dimensions** | 64-768 depending on type |
| **Key Benefit** | Captures semantic similarity, enables transfer learning |
| **Best For** | Similarity search, pattern detection, multi-modal fusion |

**Key Insight**: Embeddings are the **universal language** of modern ML. They transform diverse data types—behaviors, text communications, item interactions, graph relationships—into a common numerical format where similarity has geometric meaning. Foundation-model embeddings learn from large volumes of events to create representations that improve many downstream models. The shift from hand-crafted features to learned embeddings demonstrates the power of letting models discover optimal representations. As systems move toward more sophisticated multi-modal fusion (combining behavioral + text + graph embeddings), embeddings serve as the **connective tissue** enabling unified assessment across previously siloed data sources.

## Key Highlights

**Embedding Types and Architectures.** Modern systems employ several major embedding families: Behavioral (transformer-based multi-sequence modeling producing per-entity vectors), Graph (TGN, HGT, GraphSAGE for learning from relationship graphs), Text (BERT/DeBERTa, Word2Vec, Sentence Transformers for classification, association, and clustering), and Item/categorical (learned item embeddings, Semantic IDs via RQ-VAE). Dimensions range from 64-128 for categorical embeddings up to 768-1024 for BERT text embeddings, with update frequencies from batch to near real-time.

**Embedding Applications.** Embeddings power four core capabilities: detection enhancement (multi-modal fusion combining heterogeneous signals), entity similarity and linkage (cosine similarity for grouping related entities), anomaly detection (contrastive learning to surface outliers), and transfer learning (pre-trained embeddings fine-tuned across related domains).

**Technical Implementation and Representation Comparison.** Practical embedding creation spans three approaches: transformer-based text embeddings (BERT [CLS] token extraction), graph embeddings (GraphSAGE with multi-hop neighbor aggregation), and dimensionality reduction (UMAP achieving large reductions while preserving signal). Compared to alternatives, embeddings offer lower dimensionality (64-768 vs vocabulary-sized one-hot), preserved semantic similarity (unlike one-hot or TF-IDF), high memory efficiency, and superior transferability through pre-training.

## Related Terms

### Embedding Architectures
- **[BERT](term_bert.md)** - Bidirectional Encoder Representations from Transformers
- **[Transformer](term_transformer.md)** - Attention-based architecture
- **[GNN](term_gnn.md)** - Graph Neural Network

### Related Concepts
- **[Cosine Similarity](term_cosine_similarity.md)** - The dominant scoring function for comparing embeddings; magnitude-invariant similarity in vector space
- **[Dense Retrieval](term_dense_retrieval.md)** - The IR family that ranks documents by embedding similarity rather than lexical overlap
- **[Dimensionality Reduction](term_dimensionality_reduction.md)** - Embeddings are learned dimensionality reductions; PCA can further compress embeddings
- **[PCA](term_pca.md)** - Often used to compress embeddings for visualization or efficiency
- **[ANN Search](term_ann_search.md)** - ANN indices (FAISS, HNSW) enable efficient similarity search over embeddings
- **[RAG](term_rag.md)** - Retrieval Augmented Generation using embeddings
- **[Vector Database](term_vector_database.md)** - Specialized storage and search for embeddings
- **[Contrastive Learning](term_contrastive_learning.md)** - Learning embeddings via contrasts
- **[Pre-training](term_pretraining.md)** - Learning general representations
- **[VLM](term_vlm.md)** - Vision Language Models (visual embeddings)

### Related ML Concepts
- **[LLM](term_llm.md)** - Large Language Models (produce text embeddings)
- **[SBERT](term_sbert.md)** - Sentence-BERT for sentence-level embeddings
- **[HGT](term_hgt.md)** - Heterogeneous Graph Transformer (graph embeddings)
- **[ViT](term_vit.md)** - Vision Transformer (image embeddings)
- **[Continual Learning](term_continual_learning.md)** - Incremental model updates preserving learned embeddings

---

## References

### External Resources
- **Word2Vec Paper**: [Efficient Estimation of Word Representations](https://arxiv.org/abs/1301.3781)
- **BERT Paper**: [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- **GraphSAGE Paper**: [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216)

---

**Last Updated**: March 15, 2026
**Status**: Active - foundational technology for modern ML
