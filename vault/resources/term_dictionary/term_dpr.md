---
tags:
  - resource
  - terminology
  - machine_learning
  - information_retrieval
  - nlp
  - deep_learning
keywords:
  - DPR
  - Dense Passage Retrieval
  - bi-encoder
  - dense retrieval
  - passage retrieval
  - MIPS
  - maximum inner product search
  - open-domain QA
  - neural retriever
  - FAISS
topics:
  - Information Retrieval
  - NLP
  - Open-Domain Question Answering
  - Dense Retrieval
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
related_wiki: null
---

# DPR - Dense Passage Retrieval

## Definition

**Dense Passage Retrieval (DPR)** is a neural information retrieval method that encodes both queries and passages into dense vector representations using dual BERT encoders, then performs nearest-neighbor search in the embedding space to find relevant passages. Unlike traditional sparse retrieval methods (BM25, TF-IDF) that match exact terms, DPR captures semantic similarity — retrieving passages that are conceptually relevant even without lexical overlap.

DPR was introduced by Karpukhin et al. (2020) and became the retrieval backbone for RAG (Lewis et al., 2020). It demonstrated that dense retrieval outperforms BM25 on open-domain QA by 9-19% (in top-20 passage accuracy), establishing neural retrieval as the standard for knowledge-intensive NLP tasks.

## How DPR Works

### Bi-Encoder Architecture

DPR uses two independent BERT_BASE encoders:

```
Query Encoder:    q(x) = BERT_Q(x)[CLS]     → 768-dim vector
Document Encoder: d(z) = BERT_D(z)[CLS]     → 768-dim vector

Relevance Score:  sim(x, z) = q(x)ᵀ · d(z)  (dot product)
```

The bi-encoder architecture is critical for efficiency: all document vectors can be **pre-computed offline**, and at query time only the query needs encoding. Retrieval then reduces to Maximum Inner Product Search (MIPS).

### Training

DPR is trained with contrastive learning using in-batch negatives:

1. **Positive pairs**: (question, gold passage) from QA datasets
2. **Hard negatives**: BM25-retrieved passages that don't contain the answer (challenging non-relevant passages)
3. **In-batch negatives**: Other questions' positive passages serve as negatives
4. **Loss**: Negative log-likelihood of the positive passage

### Indexing and Search

1. **Offline**: Encode all passages with BERT_D → store vectors in FAISS index
2. **Online**: Encode query with BERT_Q → MIPS over FAISS → return top-k passages

Typical index: 21 million Wikipedia passages (100-word chunks), stored as 768-dim vectors in FAISS with HNSW approximation.

## Key Characteristics

- **Semantic Matching**: Captures meaning beyond exact word overlap — "Who wrote Hamlet?" retrieves passages about "Shakespeare authored the play"
- **Pre-computed Index**: Document vectors computed once offline; query-time cost is only query encoding + MIPS
- **Bi-Encoder Efficiency**: O(1) per-document at query time (vs cross-encoder's O(n) re-encoding)
- **Hard Negative Mining**: Training with BM25-retrieved negatives is critical for learning to distinguish truly relevant from superficially similar passages
- **FAISS Integration**: Sub-linear retrieval over millions of passages using approximate nearest neighbor search

## Performance

| Metric | DPR | BM25 | Improvement |
|--------|-----|------|-------------|
| **NQ Top-20** | 79.4% | 59.1% | +20.3% |
| **TriviaQA Top-20** | 79.4% | 66.9% | +12.5% |
| **WQ Top-20** | 73.2% | 55.0% | +18.2% |
| **TREC Top-20** | 89.1% | 70.9% | +18.2% |

DPR consistently outperforms BM25 sparse retrieval across all open-domain QA benchmarks.

## DPR vs Other Retrieval Methods

| Method | Representation | Matching | Pre-compute | Semantic |
|--------|---------------|----------|-------------|----------|
| **BM25** | Sparse (term freq) | Exact lexical | ✅ | ❌ |
| **DPR** | Dense (BERT) | Dot product | ✅ | ✅ |
| **Cross-Encoder** | Joint (BERT) | Full attention | ❌ | ✅✅ |
| **ColBERT** | Multi-vector | Late interaction | ✅ | ✅ |
| **Hybrid (DPR + BM25)** | Both | Combined | Partial | ✅ |

**Trade-off**: DPR sacrifices some precision vs cross-encoders for massive efficiency gains. In practice, hybrid approaches (DPR retrieval + cross-encoder re-ranking) often achieve the best results.

## Context

Within Buyer Risk Prevention (BRP) and Amazon more broadly, DPR-style dense retrieval underlies several key systems:

- **RAG systems**: GreenTEA, AskNexus, DeepCARE all use dense vector retrieval over internal knowledge bases
- **Amazon Bedrock Knowledge Bases**: Use dense embedding models (Titan, Cohere) for retrieval — the same architectural pattern as DPR
- **Abuse Slipbox**: The vault's graph-based retrieval is complementary to DPR-style similarity search; both are used for the answer-query pipeline
- **Similarity search**: DeepCARE's k-NN investigation retrieval follows DPR's encode-then-search paradigm

## Related Terms

- **[ANN Search](term_ann_search.md)**: DPR relies on ANN indices (FAISS) to efficiently search over millions of passage embeddings
- **[Information Retrieval](term_information_retrieval.md)**: DPR is a dense retrieval method within the broader IR field; contrasts with lexical (BM25) retrieval
- **[Product Quantization](term_product_quantization.md)**: FAISS's IVF-PQ index powers DPR's passage retrieval at scale
- **[IVF](term_ivf.md)**: DPR typically uses IVF-based FAISS indices for efficient search
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation — DPR serves as the retrieval component of RAG
- **[Embedding](term_embedding.md)**: Dense vector representations that DPR produces for queries and passages
- **[FAISS](term_faiss.md)**: Facebook AI Similarity Search — ANN index used by DPR
- **[Vector Database](term_vector_database.md)**: Storage systems (OpenSearch, Pinecone) that serve the same role as FAISS in production
- **[LLM](term_llm.md)**: Large Language Models that DPR-retrieved passages augment via RAG
- **[Knowledge Graph](term_knowledge_graph.md)**: Alternative structured retrieval; Graph-RAG extends flat passage retrieval with graph structure
- **[Transformer](term_transformer.md)**: Architecture underlying DPR's BERT encoders
- **[SBERT](term_sbert.md)**: Sentence-BERT uses similar bi-encoder architecture for sentence embeddings; DPR specializes this for passage retrieval
- **[Dense Retrieval](term_dense_retrieval.md)**: DPR is the canonical instance of the dense-retrieval IR family
- **[Cosine Similarity](term_cosine_similarity.md)**: The scoring function over the L2-normalized embeddings DPR produces (reduces to a dot product at query time)

## References

### Primary Source
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../papers/lit_lewis2020retrieval.md) — Lewis et al. (2020), NeurIPS 2020. *RAG paper that uses DPR as its retriever component.*

### Foundational Paper
- Karpukhin, V., et al. (2020). "Dense Passage Retrieval for Open-Domain Question Answering." EMNLP 2020. arXiv:2004.04906. *Original DPR paper: bi-encoder BERT, contrastive training with hard negatives, FAISS indexing.*

### Internal Documentation
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) — Managed dense retrieval service using the same architectural pattern as DPR
