---
tags:
  - resource
  - literature_note
  - information_retrieval
  - knowledge_graph
  - generative_ai
  - graph_rag
keywords:
  - GraphRAG
  - graph-based RAG
  - global sensemaking
  - query-focused summarization
  - community detection
  - Leiden algorithm
  - map-reduce summarization
  - entity knowledge graph
  - hierarchical community summaries
  - LLM-as-a-judge
  - adaptive benchmarking
topics:
  - Information Retrieval
  - Knowledge Graphs
  - Retrieval-Augmented Generation
  - Query-Focused Summarization
domain: "Retrieval-Augmented Generation"
language: markdown
date of note: 2026-03-08
paper_title: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
authors:
  - Darren Edge
  - Ha Trinh
  - Newman Cheng
  - Joshua Bradley
  - Alex Chao
  - Apurva Mody
  - Steven Truitt
  - Dasha Metropolitansky
  - Robert Osazuwa Ness
  - Jonathan Larson
year: 2024
source: "arXiv:2404.16130"
venue: "arXiv (preprint)"
DOI: ""
arXiv: "2404.16130"
semantic_scholar_id: "c1799bf28d1ae93e1631be5b59196ee1e568f538"
zotero_key: "QG7ZU5P2"
paper_id: edge2024local
paper_notes:
  - paper_edge2024local_intro.md
  - paper_edge2024local_contrib.md
  - paper_edge2024local_model.md
  - paper_edge2024local_exp_design.md
  - paper_edge2024local_exp_result.md
status: active
building_block: hypothesis
---

# Literature Note: From Local to Global — A GraphRAG Approach to Query-Focused Summarization

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | From Local to Global: A Graph RAG Approach to Query-Focused Summarization |
| **Authors** | Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, Jonathan Larson |
| **Affiliation** | Microsoft Research, Microsoft Strategic Missions and Technologies, Microsoft Office of the CTO |
| **Year** | 2024 |
| **Venue** | arXiv (preprint, under review) |
| **arXiv** | [2404.16130](https://arxiv.org/abs/2404.16130) |
| **Citations** | 1,159 (as of March 2026) |
| **Semantic Scholar** | [c1799bf28d1ae93e1631be5b59196ee1e568f538](https://www.semanticscholar.org/paper/c1799bf28d1ae93e1631be5b59196ee1e568f538) |
| **Zotero** | QG7ZU5P2 |
| **Open Source** | [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag) |

## Abstract

The use of retrieval-augmented generation (RAG) to retrieve relevant information from an external knowledge source enables large language models (LLMs) to answer questions over private and/or previously unseen document collections. However, RAG fails on global questions directed at an entire text corpus, such as "What are the main themes in the dataset?", since this is inherently a query-focused summarization (QFS) task, rather than an explicit retrieval task. Prior QFS methods, meanwhile, do not scale to the quantities of text indexed by typical RAG systems. To combine the strengths of these contrasting methods, we propose GraphRAG, a graph-based approach to question answering over private text corpora that scales with both the generality of user questions and the quantity of source text. Our approach uses an LLM to build a graph index in two stages: first, to derive an entity knowledge graph from the source documents, then to pregenerate community summaries for all groups of closely related entities. Given a question, each community summary is used to generate a partial response, before all partial responses are again summarized in a final response to the user. For a class of global sensemaking questions over datasets in the 1 million token range, we show that GraphRAG leads to substantial improvements over a conventional RAG baseline for both the comprehensiveness and diversity of generated answers.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_edge2024local_intro](paper_edge2024local_intro.md) | Vector RAG fails on global sensemaking; QFS doesn't scale; research gap in graph-community RAG |
| **Contribution** | [paper_edge2024local_contrib](paper_edge2024local_contrib.md) | 3 contributions: GraphRAG method, adaptive benchmarking, empirical demonstration; novelty in community-based summarization |
| **Model** | [paper_edge2024local_model](paper_edge2024local_model.md) | 6-stage indexing pipeline (chunks→entities→KG→communities→summaries); map-reduce query answering; Leiden hierarchy; self-reflection for extraction |
| **Experiment Design** | [paper_edge2024local_exp_design](paper_edge2024local_exp_design.md) | 2 datasets (~1-1.7M tokens); 6 conditions (C0-C3, TS, SS); LLM-as-a-judge + claim-based metrics |
| **Experiment Result** | [paper_edge2024local_exp_result](paper_edge2024local_exp_result.md) | 72-83% comprehensiveness win rate; 62-82% diversity; 97% token reduction at root; claim validation aligns 78% |
| **Review** | [review_edge2024local](review_edge2024local.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY -->
**Introduction**: Vector RAG retrieves locally relevant chunks but cannot answer global sensemaking questions requiring corpus-wide understanding. Prior QFS methods don't scale to RAG-sized corpora. No existing approach uses graph community structure for hierarchical summarization.

**Contribution**: GraphRAG is the first system to combine LLM-derived entity knowledge graphs + Leiden community detection + hierarchical community summaries + map-reduce answering for global sensemaking over large text corpora. It also proposes adaptive benchmarking via persona-generated sensemaking questions with LLM-as-a-judge evaluation.

**Model**: The offline pipeline extracts entities and relationships via GPT-4-turbo (with self-reflection for improved recall), constructs a knowledge graph, partitions it hierarchically using Leiden, and pre-generates community summaries at each level. The online pipeline shuffles and chunks community summaries, generates partial answers in parallel (map), filters by helpfulness score, and synthesizes a global answer (reduce).

**Results**: GraphRAG achieves 72-83% comprehensiveness and 62-82% diversity win rates over vector RAG across two 1M+ token datasets. Root-level community summaries (C0) achieve competitive performance at 97%+ fewer tokens. Claim-based metrics validate the LLM judgments with 78% agreement.

## Relevance to Our Work

- [RAG](../term_dictionary/term_rag.md) — GraphRAG extends the foundational RAG paradigm toward global sensemaking, complementary to the factual RAG in Lewis et al. 2020
- [Knowledge Graph](../term_dictionary/term_knowledge_graph.md) — LLM-derived entity knowledge graph is the core index structure; relevant to Nexus's KG approach
- [Community Detection](../term_dictionary/term_community_detection.md) — Leiden community detection is central to the method; community-based organization could structure abuse knowledge
- [HippoRAG](../term_dictionary/term_hipporag.md) — Complementary graph-RAG approach using PPR over open KG; HippoRAG focuses on multi-hop factual retrieval, GraphRAG on global summarization
- [Nexus](../../areas/area_nexus.md) — BRP's graph-RAG system; community summarization and hierarchical query patterns are directly applicable
- [LLM](../term_dictionary/term_llm.md) — GPT-4-turbo used throughout; the approach could be adapted to smaller models
- [Embedding](../term_dictionary/term_embedding.md) — Vector RAG baseline uses embedding similarity; GraphRAG replaces this with community-based retrieval

## Questions

1. How does GraphRAG perform on local/multi-hop factual questions (the domain where HippoRAG 2 excels)?
2. Can the community summarization approach be combined with PPR-based retrieval (HippoRAG) for a system that handles both local and global queries?
3. What is the fabrication rate in community summaries? Do LLM-generated summaries introduce facts not in the source?
4. How sensitive is the system to entity extraction quality? What happens with a smaller LLM (e.g., Llama-3.3-70B)?
5. Could the community hierarchy be built incrementally as new documents arrive (continual learning scenario)?

## Related Literature

- [lit_lewis2020retrieval](lit_lewis2020retrieval.md) — RAG: the foundational retrieval-augmented generation paper that GraphRAG extends
- [lit_gutierrez2025rag](lit_gutierrez2025rag.md) — HippoRAG 2: complementary graph-RAG approach using PPR + dense-sparse coding
- [lit_gao2025survey](lit_gao2025survey.md) — Survey of RAG approaches including graph-based methods

## Related Documentation

- [Nexus](../../areas/area_nexus.md) — BRP's production graph-RAG system
- [Nexus Project](../../projects/project_nexus.md) — Active Nexus development project
