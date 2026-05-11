---
tags:
  - resource
  - terminology
  - machine_learning
  - information_retrieval
  - graph_algorithms
keywords:
  - HippoRAG
  - HippoRAG 2
  - hippocampal indexing theory
  - graph RAG
  - associative memory
  - knowledge graph
  - Personalized PageRank
topics:
  - retrieval-augmented generation
  - knowledge graphs
  - information retrieval
  - neuroscience-inspired AI
language: markdown
date of note: 2026-03-03
status: active
building_block: concept
related_wiki: null
---

# HippoRAG - Hippocampus-inspired Retrieval-Augmented Generation

## Definition
HippoRAG is a retrieval-augmented generation framework inspired by the hippocampal indexing theory of human long-term memory. It models the interaction between the neocortex (LLM for processing), the hippocampus (knowledge graph for indexing), and the entorhinal cortex (retrieval encoder for pattern separation) to enable deeper knowledge integration across documents. Unlike standard RAG which retrieves isolated text chunks via embedding similarity, HippoRAG constructs a persistent knowledge graph using LLM-based Open Information Extraction (OpenIE) and retrieves relevant subgraphs using Personalized PageRank (PPR), enabling multi-hop reasoning and associative memory across passages.

## Context
HippoRAG was introduced as a NeurIPS 2024 paper (arXiv:2405.14831) by researchers at OSU. It addresses a fundamental limitation of standard RAG: the inability to integrate knowledge across multiple passages for complex reasoning tasks. At Amazon, GraphRAG approaches are actively explored by the DS3 gRAG team (Vassilis Ioannidis, Qi Zhu, Costas Mavromatis) through the Mercury framework, and by teams like AB Search (Cibeles) who use PPR-based graph retrieval in production hybrid search systems. HippoRAG's architecture is directly relevant to BRP knowledge systems that need to connect abuse patterns across disparate documents, investigations, and historical cases.

## Key Characteristics
- **Neurobiological Architecture**: Maps three brain components to computational analogs — neocortex (LLM for processing), hippocampal index (knowledge graph for associative linking), entorhinal cortex (retrieval encoder for pattern separation)
- **Knowledge Graph Construction**: Uses LLM-based OpenIE to extract (subject, predicate, object) triples from passages, building a persistent schemaless KG that grows with new documents
- **PPR-based Retrieval**: Seeds Personalized PageRank from query-matched entities to traverse the KG and retrieve contextually relevant nodes across multiple hops, enabling associative recall
- **Continual Learning**: New passages are incrementally added to the KG without retraining, mimicking non-parametric memory consolidation
- **HippoRAG 2 Extensions**: Integrates dense-sparse passage nodes into the KG, adds query-to-triple linking for deeper contextualization, and introduces LLM-based recognition memory — first RAG system to outperform standard dense retrieval across factual, sense-making, and associative memory dimensions
- **Multi-hop Reasoning**: Excels at questions requiring synthesis across multiple documents where standard chunk-based RAG fails

## Performance / Metrics
- Outperforms standard RAG by up to 20% on multi-hop QA benchmarks (MuSiQue, 2WikiMultiHopQA)
- HippoRAG 2 is the first RAG system to surpass dense retrieval across all three memory dimensions
- Published at NeurIPS 2024 with open-source code and data

## Related Terms
- **[ANN Search](term_ann_search.md)**: HippoRAG combines graph traversal (PPR) with ANN-based embedding retrieval for hybrid search
- **[RAG](term_rag.md)**: Standard retrieval-augmented generation that HippoRAG extends with graph-based knowledge integration
- **[GraphRAG](term_graphrag.md)**: Complementary graph-RAG approach (Edge et al., 2024) using community detection + hierarchical summarization
- **[PPR](term_ppr.md)**: Personalized PageRank algorithm used as the core retrieval mechanism in HippoRAG's hippocampal index
- **[PageRank](term_pagerank.md)**: Parent algorithm of PPR; HippoRAG's associative retrieval inherits the eigenvector-centrality framing from this
- **[Random Walk](term_random_walk.md)**: The stochastic process whose stationary distribution PPR computes — the substrate HippoRAG's "associative memory" lookup runs over
- **[Dense Retrieval](term_dense_retrieval.md)**: HippoRAG 2 adds dense-sparse passage integration on top of the PPR-based associative retrieval
- **[Cosine Similarity](term_cosine_similarity.md)**: Scoring function used by the dense passages HippoRAG combines with graph retrieval
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured entity-relationship representation that serves as HippoRAG's persistent memory store
- **[LLM](term_llm.md)**: Large Language Models used for both knowledge extraction (OpenIE) and answer generation in the HippoRAG pipeline
- **[DPR](term_dpr.md)**: Dense Passage Retrieval — baseline retriever that HippoRAG's PPR-based approach aims to surpass
- **[Community Detection](term_community_detection.md)**: Graph partitioning technique used in GraphRAG (Leiden) and potentially combinable with HippoRAG's PPR retrieval

## References
- [HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs (arXiv:2405.14831)](https://arxiv.org/abs/2405.14831)
  - Source: [lit_gutierrez2025rag](../papers/lit_gutierrez2025rag.md) — first encountered in this paper
- [RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)](../papers/lit_lewis2020retrieval.md) — foundational RAG paper that HippoRAG extends
- [GraphRAG: From Local to Global (Edge et al., 2024)](../papers/lit_edge2024local.md) — complementary graph-RAG approach using community detection for global sensemaking
- [TFL GraphRAG - Amazon AI Research](https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/TFL-GraphRAG/)
- [GraphRAG AMLC 2024 Tutorial](https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/TFL-GraphRAG/GraphRAGAMLC2024/)

