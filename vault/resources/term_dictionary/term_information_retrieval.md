---
tags:
  - resource
  - terminology
  - information_retrieval
  - search
  - nlp
  - ranking
keywords:
  - information retrieval
  - IR
  - search
  - relevance
  - precision
  - recall
  - BM25
  - TF-IDF
  - inverted index
  - dense retrieval
  - neural IR
topics:
  - Information Retrieval
  - Search Systems
  - Natural Language Processing
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# Information Retrieval (IR)

## Definition

**Information Retrieval (IR)** is the field concerned with finding documents, passages, or data objects relevant to an information need from a large collection. Unlike database queries that return exact matches, IR systems **rank results by relevance** — a fundamental distinction that makes IR probabilistic and evaluation-dependent. The field was named by **Calvin Mooers (1950)** and formalized by **Gerard Salton** in the 1960s with the vector space model.

Modern IR encompasses both **lexical methods** (BM25, TF-IDF via inverted indices) and **dense/neural methods** (DPR, ColBERT via vector embeddings + ANN search), with hybrid approaches combining both for production search systems.

## Historical Context

| Year | Milestone |
|------|-----------|
| 1950 | **Mooers** coins "information retrieval" |
| 1960s | **Salton** develops vector space model and TF-IDF at Cornell |
| 1977 | **Robertson & Spärck Jones** develop probabilistic IR (BM25 precursor) |
| 1992 | **TREC** established — standardized large-scale IR evaluation |
| 1998 | **PageRank** (Brin & Page) transforms web search via link analysis |
| 2019 | **BERT** applied to IR (Nogueira & Cho) — neural re-ranking |
| 2020 | **DPR** (Karpukhin et al.) — dense retrieval via dual-encoder BERT |
| 2020 | **RAG** (Lewis et al.) — retrieval-augmented generation connects IR to LLMs |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Inverted Index** | Maps terms → document lists; core data structure for lexical retrieval |
| **TF-IDF** | Term frequency × inverse document frequency; measures term importance |
| **BM25** | Probabilistic ranking function; the dominant lexical retrieval baseline |
| **Precision** | Fraction of retrieved documents that are relevant |
| **Recall** | Fraction of relevant documents that are retrieved |
| **nDCG** | Normalized Discounted Cumulative Gain; graded relevance metric |
| **Dense Retrieval** | Encode queries and documents as vectors; retrieve via ANN search |
| **Re-ranking** | Score candidate documents with a cross-encoder for improved precision |

## Taxonomy

| Paradigm | Method | Strengths | Weaknesses |
|----------|--------|-----------|------------|
| **Lexical** | BM25 / TF-IDF | Exact term matching, interpretable, fast | Vocabulary mismatch (synonyms miss) |
| **Dense** | DPR / ColBERT | Semantic matching, handles paraphrases | Requires embedding computation + ANN index |
| **Learned Sparse** | SPLADE / DeepImpact | Semantic + interpretable + inverted index compatible | Requires training |
| **Hybrid** | BM25 + Dense | Best of both — lexical precision + semantic recall | More complex pipeline |
| **Generative** | RAG | LLM generates answer grounded in retrieved docs | Hallucination risk, latency |

## Applications

| Domain | Application |
|--------|-------------|
| **Web search** | Google, Bing — billions of queries/day |
| **RAG** | Retrieval-augmented generation for LLMs; IR provides the "R" |
| **Enterprise search** | Internal document search (wikis, emails, tickets) |
| **Legal/Medical** | Case law retrieval, clinical evidence search |
| **E-commerce** | Product search, review search |
| **Abuse detection** | Searching historical investigation records, SOP retrieval for ARI agents |

## Related Terms

- **[Dense Retrieval](term_dense_retrieval.md)**: The IR family that ranks by vector similarity in learned embedding space rather than lexical overlap
- **[Cosine Similarity](term_cosine_similarity.md)**: The dominant scoring function for dense retrieval and contrastive embedding training
- **[PageRank](term_pagerank.md)**: Graph-based importance algorithm that ranks IR results by link structure (the original web-search application)
- **[PPR](term_ppr.md)**: Personalized PageRank — query-relative graph importance for retrieval
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation — IR provides the retrieval component for LLM grounding
- **[DPR](term_dpr.md)**: Dense Passage Retrieval — neural IR using dual-encoder BERT embeddings
- **[ANN Search](term_ann_search.md)**: ANN indices (FAISS, HNSW) power dense retrieval at scale
- **[IVF](term_ivf.md)**: Inverted File Index for vector search; borrows the "inverted index" concept from text IR
- **[FTS5](term_fts5.md)**: SQLite's embedded full-text search; concrete realization of sparse-IR primitives (inverted index + BM25) inside a SQL engine
- **[Product Quantization](term_product_quantization.md)**: PQ enables memory-efficient dense retrieval via compressed vectors
- **[LSH](term_lsh.md)**: Hash-based ANN for approximate retrieval
- **[Vector Database](term_vector_database.md)**: Modern IR systems use vector databases for dense retrieval
- **[FAISS](term_faiss.md)**: ANN library powering dense retrieval at scale
- **[GraphRAG](term_graphrag.md)**: Graph-enhanced retrieval combining knowledge graphs with IR
- **[HippoRAG](term_hipporag.md)**: RAG system combining PPR graph traversal with dense retrieval
- **[Embedding](term_embedding.md)**: Dense retrieval relies on learned embeddings for semantic matching
- **[LLM](term_llm.md)**: LLMs consume IR results in RAG pipelines and can serve as re-rankers
- **[BERT](term_bert.md)**: Foundation for modern neural IR (DPR, ColBERT, cross-encoder re-ranking)
- **[Question Type Classification](term_question_type_classification.md)**: 10-category question taxonomy for evaluating IR performance per information need type

## References

### External Sources

- [Manning, C.D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press](https://nlp.stanford.edu/IR-book/) — Standard textbook
- [Robertson, S. & Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." Foundations and Trends in IR](https://doi.org/10.1561/1500000019) — BM25 survey
- [Wikipedia: Information Retrieval](https://en.wikipedia.org/wiki/Information_retrieval)
