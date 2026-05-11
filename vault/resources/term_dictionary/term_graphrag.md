---
tags:
  - resource
  - terminology
  - machine_learning
  - information_retrieval
  - knowledge_graph
  - generative_ai
keywords:
  - GraphRAG
  - graph-based RAG
  - community summarization
  - global sensemaking
  - query-focused summarization
  - Leiden algorithm
  - map-reduce
  - hierarchical graph index
  - entity knowledge graph
topics:
  - Information Retrieval
  - Knowledge Graphs
  - Retrieval-Augmented Generation
  - Query-Focused Summarization
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
related_wiki: null
---

# Term: GraphRAG

## Definition

**GraphRAG** is a graph-based retrieval-augmented generation framework (Edge et al., 2024, Microsoft Research) that answers **global sensemaking questions** over large text corpora by combining LLM-derived entity knowledge graphs with hierarchical community detection and map-reduce summarization. Unlike standard vector RAG (which retrieves locally relevant chunks) or other graph-RAG approaches (which use graph structure for retrieval), GraphRAG uniquely exploits graph **community structure** for pre-computed hierarchical summarization, enabling corpus-wide question answering at multiple levels of granularity.

## Full Name

GraphRAG — Graph-Based Retrieval-Augmented Generation

## How It Works

### Architecture Overview

```
Source Documents → Text Chunks → Entity Extraction (LLM) → Knowledge Graph
                                                              ↓
                                                    Leiden Community Detection
                                                              ↓
                                                    Hierarchical Communities
                                                              ↓
                                                    Community Summaries (LLM)
                                                              ↓
Query → Select Community Level → Map (parallel partial answers) → Reduce (global answer)
```

### Offline Indexing Pipeline

1. **Text Chunking**: Split documents into 600-token chunks with 100-token overlaps
2. **Entity & Relationship Extraction**: LLM (GPT-4-turbo) extracts named entities, relationships, and claims from each chunk using domain-tailored few-shot prompts with self-reflection for improved recall
3. **Knowledge Graph Construction**: Aggregate entity/relationship instances via string matching into nodes and weighted edges
4. **Community Detection**: Leiden algorithm (Traag et al., 2019) recursively partitions the graph into a hierarchy of communities — from root-level (broadest themes) to leaf-level (specific subtopics)
5. **Community Summary Generation**: LLM generates report-like summaries for each community, bottom-up through the hierarchy

### Online Query Pipeline

1. **Map**: Community summaries at the chosen level are shuffled, chunked, and processed in parallel by the LLM to generate partial answers with helpfulness scores (0-100)
2. **Filter**: Score-0 answers removed
3. **Reduce**: Remaining partial answers sorted by helpfulness, iteratively packed into context window, and synthesized into a final global answer

## Key Distinction: GraphRAG vs. Other Graph-RAG Systems

| Feature | GraphRAG (Edge et al.) | HippoRAG 2 (Gutierrez et al.) | LightRAG | Vector RAG |
|---------|----------------------|------------------------------|----------|------------|
| **Primary query type** | Global sensemaking | Multi-hop factual | Local + structured | Local factual |
| **Graph use** | Community summarization | PPR-based retrieval | Dual-level retrieval | None |
| **KG construction** | LLM entity extraction | LLM OpenIE triples | LLM + embedding | N/A |
| **Community detection** | Leiden (hierarchical) | None | None | None |
| **Pre-computation** | Community summaries at all levels | None (online PPR) | None | Embeddings only |
| **Token efficiency** | 97% reduction at root vs. source text | Standard | Standard | Standard |
| **Online LLM calls** | Map-reduce answering | Triple filtering | None | Generation only |

## Performance

### Head-to-Head Win Rates vs. Vector RAG

| Metric | Podcast (~1M tokens) | News (~1.7M tokens) |
|--------|---------------------|---------------------|
| Comprehensiveness | **72-83%** (p<.001) | **72-80%** (p<.001) |
| Diversity | **75-82%** (p<.001) | **62-71%** (p<.01) |
| Directness | 35-40% (vector RAG wins) | 41-46% (vector RAG wins) |

### Token Efficiency by Community Level

| Level | Tokens (% of source) | Use Case |
|-------|---------------------|----------|
| C0 (root) | **2-3%** | Iterative exploration, theme discovery |
| C1 | 20-22% | High-level analysis |
| C2 | 55-57% | Balanced detail/scope |
| C3 (leaf) | 67-74% | Detailed analysis |
| Source text | 100% | Maximum comprehensiveness |

### Graph Index Scale

| Dataset | Nodes | Edges | Communities (C0/C1/C2/C3) |
|---------|-------|-------|--------------------------|
| Podcast (~1M tokens) | 8,564 | 20,691 | 34 / 367 / 969 / 1,310 |
| News (~1.7M tokens) | 15,754 | 19,520 | 55 / 555 / 1,797 / 2,142 |

## Strengths

1. **Enables new query type**: Only system that can answer corpus-wide sensemaking questions at scale
2. **Multi-granularity**: Community hierarchy provides natural cost-quality trade-off (root for cheap exploration, leaf for detail)
3. **Token efficient**: Root-level summaries achieve competitive comprehensiveness at 97%+ fewer tokens
4. **Modular design**: Each pipeline stage (extraction, community detection, summarization, answering) can be independently improved
5. **Open source**: [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)

## Limitations

1. **Not designed for local queries**: May underperform vector RAG on factual, multi-hop, or entity-specific questions
2. **High indexing cost**: Requires GPT-4-turbo for entity extraction and summary generation (281 min for 1M tokens)
3. **Fabrication risk**: Community summaries are LLM-generated abstractions — may introduce facts not in source
4. **Entity resolution**: Uses exact string matching; may create duplicate nodes without soft matching
5. **Only tested on 2 datasets**: Generalization to other domains and scales unknown
6. **GPT-4-turbo dependency**: Performance with smaller or open-source LLMs not evaluated

## BRP Context

### Potential Applications

- **Nexus Enhancement**: Community summarization could provide Nexus with global abuse theme summaries across the knowledge graph
- **Abuse Slipbox Agent**: The map-reduce query pattern could improve answering broad questions like "What are the main abuse trends?" across the entire vault
- **Investigation Support**: Hierarchical community summaries could organize abuse pattern documentation at different granularities (program → type → instance)
- **Tattletale Integration**: The existing community detection in Tattletale could be extended with LLM-generated community summaries for richer investigator context

### Hybrid Approach Opportunity

A practical deployment could combine:
- **GraphRAG** for global/thematic questions ("What are the main abuse patterns across all programs?")
- **HippoRAG / Vector RAG** for local/factual questions ("What is the refund rate for DNR in Q4?")
- **Community level selection** as a dynamic parameter based on query type classification

## Related Terms

- [RAG](term_rag.md) — The foundational retrieval-augmented generation paradigm that GraphRAG extends
- [Knowledge Graph](term_knowledge_graph.md) — LLM-derived entity KG is the core index structure
- [Community Detection](term_community_detection.md) — Leiden algorithm partitions the graph into hierarchical communities
- [HippoRAG](term_hipporag.md) — Complementary graph-RAG approach using PPR over open KG for multi-hop retrieval
- [PPR](term_ppr.md) — Personalized PageRank, the alternative graph-traversal primitive HippoRAG uses (contrast with GraphRAG's Leiden-community approach)
- [PageRank](term_pagerank.md) — The parent graph-importance algorithm; descendants underlie the graph-RAG family GraphRAG belongs to
- [Random Walk](term_random_walk.md) — Random-walk-based importance is one of two main families of graph-RAG retrieval (the other being community detection that GraphRAG uses)
- [Dense Retrieval](term_dense_retrieval.md) — The vector-RAG baseline GraphRAG outperforms on global sensemaking
- [LLM](term_llm.md) — GPT-4-turbo serves triple role: entity extraction, summary generation, query answering
- [Embedding](term_embedding.md) — Vector embeddings used in the baseline vector RAG comparison
- [DPR](term_dpr.md) — Dense Passage Retrieval used in the vector RAG baseline
- [Nexus](term_nexus.md) — BRP's graph-RAG system that could adopt community summarization
- [Hallucination](term_hallucination.md) — Community summaries may introduce fabricated details (unquantified risk)

## References

- **Primary Source**: [lit_edge2024local](../papers/lit_edge2024local.md) — Edge et al. (2024), "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
- **Related Work**: [lit_gutierrez2025rag](../papers/lit_gutierrez2025rag.md) — HippoRAG 2: complementary graph-RAG using PPR
- **Related Work**: [lit_lewis2020retrieval](../papers/lit_lewis2020retrieval.md) — RAG: the foundational paper
- **Open Source**: [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)
- **Leiden Algorithm**: Traag, V. A., Waltman, L., & Van Eck, N. J. (2019). "From Louvain to Leiden: guaranteeing well-connected communities." Scientific Reports, 9(1).
