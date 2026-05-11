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
  - buyer risk prevention
  - machine learning
  - deep learning
  - representation learning
  - fraud detection
language: markdown
date of note: 2026-02-08
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/Sandstone/
---

# Embedding

## Definition

**Embedding** is a learned dense vector representation that maps high-dimensional discrete data (words, customers, ASINs, events) into a continuous, lower-dimensional vector space where semantic similarities are preserved as geometric distances. At Amazon/BRP, embeddings are foundational to fraud and abuse detection—transforming customer behaviors, text data (BSM, CS contacts), product interactions, and graph relationships into fixed-size numerical vectors that ML models can process. The key insight is that entities with similar characteristics or behaviors cluster together in embedding space, enabling powerful downstream tasks like classification, similarity search, and anomaly detection.

**Key Function**: Convert discrete, high-cardinality data into continuous numerical representations that capture semantic meaning and enable ML models to learn patterns for fraud/abuse detection.

## Summary

**Embedding Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Definition** | Dense vector representation mapping discrete data to continuous space |
| **Key Types at BRP** | Behavioral (Sandstone), Graph (TGN/COSA), Text (BERT), Product (ASIN) |
| **Typical Dimensions** | 64-768 depending on type |
| **Key Benefit** | Captures semantic similarity, enables transfer learning |
| **Production Systems** | Sandstone FBM, COSA-HGT, CrossBERT, DeepCARE |
| **Best For** | Customer similarity, fraud pattern detection, multi-modal fusion |

**Key Insight**: Embeddings are the **universal language** of modern ML at BRP. They transform diverse data types—customer behaviors, text communications, product interactions, graph relationships—into a common numerical format where similarity has geometric meaning. **Sandstone** represents BRP's strategic investment in foundation model embeddings, learning from billions of customer events to create representations that improve fraud detection across dozens of downstream models. The shift from hand-crafted features to learned embeddings (e.g., CrossBERT's +160 BPS improvement over concatenated inputs) demonstrates the power of letting models discover optimal representations. As BRP moves toward more sophisticated multi-modal fusion (combining Sandstone + text + graph embeddings), embeddings serve as the **connective tissue** enabling unified risk assessment across previously siloed data sources.

## Key Highlights

**Embedding Types and Architectures at BRP.** BRP employs four major embedding families: Behavioral (Sandstone FBM using transformer-based multi-sequence modeling with 768-D customer vectors), Graph (TGN, SMAUG, HGT, GraphSAGE for learning from customer-attribute and customer-ASIN relationship graphs), Text (BERT/DeBERTa, CrossBERT, Word2Vec, Sentence Transformers for BSM classification, identity association, and CS chat clustering), and Product (M5 ASIN embeddings, Semantic IDs via RQ-VAE). Dimensions range from 64-128 for categorical embeddings up to 768-1024 for BERT text embeddings, with update frequencies from batch to near real-time. See [Embedding Types at BRP](../analysis_thoughts/thought_embedding_types_at_brp.md) for full details.

**Embedding Applications and Project Impact.** Embeddings power four core BRP capabilities: fraud detection enhancement (MVAE fusion yielding ~400 BPS improvement for fake content detection; Sandstone + TSA embeddings providing +30 BPS), customer similarity and linkage (cosine similarity for abuse ring detection), anomaly detection (DCL contrastive learning delivering +78 BPS ATO Recall@1%FPR), and transfer learning (pre-trained embeddings fine-tuned across fraud domains). Key projects include Sandstone (2024-2026 foundation model), TGN/COSA (+20% ATO capture), CrossBERT (+54/160 BPS fraud/abuse AUC), and MODES (95% dimension reduction with maintained performance). See [Embedding Applications at BRP](../analysis_thoughts/thought_embedding_applications_at_brp.md) for full details.

**Technical Implementation and Representation Comparison.** Practical embedding creation spans three approaches: transformer-based text embeddings (BERT [CLS] token extraction), graph embeddings (GraphSAGE with multi-hop neighbor aggregation), and dimensionality reduction (UMAP/MODES achieving 95% reduction while preserving fraud signal). Compared to alternatives, embeddings offer lower dimensionality (64-768 vs vocabulary-sized one-hot), preserved semantic similarity (unlike one-hot or TF-IDF), high memory efficiency, and superior transferability through pre-training. See [Embedding Technical Implementation](../policy_sops/sop_embedding_implementation.md) and [Embedding vs Other Representations](../analysis_thoughts/thought_embedding_vs_other_representations.md) for full details.

## See Also

### Model and Empirical Analysis
- **[Embedding Types at BRP](../analysis_thoughts/thought_embedding_types_at_brp.md)** - Behavioral (Sandstone), Graph (TGN/SMAUG/HGT), Text (BERT/CrossBERT), Product (ASIN) embedding architectures, dimensions, and update frequencies
- **[Embedding Applications at BRP](../analysis_thoughts/thought_embedding_applications_at_brp.md)** - Fraud detection enhancement, customer similarity and linkage, anomaly detection, transfer learning, key BRP project impact table
- **[Embedding vs Other Representations](../analysis_thoughts/thought_embedding_vs_other_representations.md)** - Comparison of embeddings against one-hot encoding and TF-IDF across dimensionality, similarity, efficiency, and transferability

### Procedures
- **[Embedding Technical Implementation](../policy_sops/sop_embedding_implementation.md)** - Code examples for creating text embeddings with BERT, graph embeddings with GraphSAGE, and dimensionality reduction with UMAP/MODES

## Related Terms

### Embedding Architectures
- **[BERT](term_bert.md)** - Bidirectional Encoder Representations from Transformers
- **[Transformer](term_transformer.md)** - Attention-based architecture
- **[GNN](term_gnn.md)** - Graph Neural Network

### BRP Embedding Systems
- **[Sandstone](term_sandstone.md)** - Foundational Behavioral Model
- **[COSA](term_cosa.md)** - Continuous One Step Ahead (graph-based)
- **[DeepCARE](term_deepcare.md)** - Uses embeddings for fraud automation

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
- **[NEAT](term_neat.md)** - NLP-based investigation automation using BERT embeddings
- **[CSMO](term_csmo.md)** - CS Chat MO detection using SBERT embeddings

---

## References

### Amazon Internal
- **Sandstone Wiki**: https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/Sandstone/
- **FBM Creator**: https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/Sandstone/Projects/FBMCreator/
- **TGN and SMAUG**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/StructuralMaskGNN/
- **GNN for Buyer Fraud**: https://w.amazon.com/bin/view/Users/xaxiao/
- **BSM Transformer Classification**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_BuyerSellerMessaging/transformer_based_classification/
- **AMLC 2023 GML Workshop**: https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/AGML/AMLC2023-GMLWorkshop/

### External Resources
- **Word2Vec Paper**: [Efficient Estimation of Word Representations](https://arxiv.org/abs/1301.3781)
- **BERT Paper**: [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- **GraphSAGE Paper**: [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216)

---

**Last Updated**: March 15, 2026
**Status**: Active - foundational technology for ML at BRP
