---
tags:
  - resource
  - literature_note
  - retrieval_augmented_generation
  - continual_learning
  - knowledge_graph
keywords:
  - HippoRAG
  - RAG
  - non-parametric continual learning
  - knowledge graph
  - Personalized PageRank
  - associative memory
  - long-term memory
topics:
  - information retrieval
  - retrieval-augmented generation
  - continual learning for LLMs
domain: "Retrieval-Augmented Generation"
language: python
date of note: 2026-03-03
paper_title: "From RAG to Memory: Non-Parametric Continual Learning for Large Language Models"
authors:
  - Bernal Jimenez Gutierrez
  - Yiheng Shu
  - Weijian Qi
  - Sizhe Zhou
  - Yu Su
year: 2025
source: "arXiv:2502.14802"
venue: "International Conference on Machine Learning (ICML)"
DOI: "10.48550/arXiv.2502.14802"
arXiv: "2502.14802"
semantic_scholar_id: "b79b3a401119bc610b6e2db738aeee531b40aaf0"
zotero_key: "GUC5UG86"
paper_id: gutierrez2025rag
paper_notes:
  - papers/paper_gutierrez2025rag_intro.md
  - papers/paper_gutierrez2025rag_contrib.md
  - papers/paper_gutierrez2025rag_model.md
  - papers/paper_gutierrez2025rag_exp_design.md
  - papers/paper_gutierrez2025rag_exp_result.md
status: active
building_block: hypothesis
---

# HippoRAG 2 — From RAG to Memory

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | From RAG to Memory: Non-Parametric Continual Learning for Large Language Models |
| **Authors** | Gutierrez, Shu, Qi, Zhou, Su |
| **Year** | 2025 |
| **Venue** | ICML 2025 |
| **DOI** | 10.48550/arXiv.2502.14802 |
| **arXiv** | 2502.14802 |
| **Citations** | 95 |

## Abstract

Our ability to continuously acquire, organize, and leverage knowledge is a key feature of human intelligence that AI systems must approximate to unlock their full potential. Given the challenges in continual learning with large language models (LLMs), retrieval-augmented generation (RAG) has become the dominant way to introduce new information. However, its reliance on vector retrieval hinders its ability to mimic the dynamic and interconnected nature of human long-term memory. Recent RAG approaches augment vector embeddings with various structures like knowledge graphs to address some of these gaps, namely sense-making and associativity. However, their performance on more basic factual memory tasks drops considerably below standard RAG. We address this unintended deterioration and propose HippoRAG 2, a framework that outperforms standard RAG comprehensively on factual, sense-making, and associative memory tasks. HippoRAG 2 builds upon the Personalized PageRank algorithm used in HippoRAG and enhances it with deeper passage integration and more effective online use of an LLM. This combination pushes this RAG system closer to the effectiveness of human long-term memory, achieving a 7% improvement in associative memory tasks over the state-of-the-art embedding model while also exhibiting superior factual knowledge and sense-making memory capabilities. This work paves the way for non-parametric continual learning for LLMs.

## Table of Contents

| Paper Section | Note | Key Content |
|---------------|------|-------------|
| Introduction, Related Work | [paper_gutierrez2025rag_intro](paper_gutierrez2025rag_intro.md) | RAG limitations for human-like memory, research gap in structure-augmented RAG |
| Contributions | [paper_gutierrez2025rag_contrib](paper_gutierrez2025rag_contrib.md) | Three-dimensional memory improvement, HippoRAG 2 novelty claims |
| HippoRAG 2 Architecture | [paper_gutierrez2025rag_model](paper_gutierrez2025rag_model.md) | Dense-sparse integration, query-to-triple linking, recognition memory, PPR |
| Datasets, Baselines, Metrics | [paper_gutierrez2025rag_exp_design](paper_gutierrez2025rag_exp_design.md) | 7 datasets across 3 memory dimensions, 10 baselines |
| Results, Ablations, Analysis | [paper_gutierrez2025rag_exp_result](paper_gutierrez2025rag_exp_result.md) | +7% associative memory, +4.8% recall@5, robustness to corpus expansion |
| Review | [review_gutierrez2025rag](review_gutierrez2025rag.md) | OpenReview-style evaluation with cross-paper similarity search |

## Summary

<!-- VERIFY: Review each summary sentence against the paper. These are AI-generated. -->

- **Background**: Standard RAG relies on vector retrieval which cannot capture sense-making and associative properties of human long-term memory. Existing structure-augmented RAG methods (RAPTOR, GraphRAG, LightRAG, HippoRAG) improve on these but deteriorate on basic factual memory tasks.
- **Contribution**: HippoRAG 2 is the first RAG framework to outperform standard RAG comprehensively across all three memory dimensions (factual, sense-making, associative) without trade-offs.
- **Method**: The system integrates passage nodes into the knowledge graph (dense-sparse coding), uses query-to-triple linking instead of NER-to-node, and adds LLM-based recognition memory for online triple filtering, all orchestrated via Personalized PageRank.
- **Results**: Achieves 7% improvement on associative memory tasks, 4.8% improvement on recall@5 over NV-Embed-v2, and maintains consistent gains under corpus expansion (continual learning simulation).

## Relevance to Our Work

- Related: [RAG](../term_dictionary/term_rag.md) — HippoRAG 2 advances RAG beyond simple vector retrieval
- Related: [Knowledge Graph](../term_dictionary/term_knowledge_graph.md) — Uses open knowledge graphs for structured retrieval
- Related: [Continual Learning](../term_dictionary/term_continual_learning.md) — Non-parametric continual learning as alternative to fine-tuning
- Related: [Nexus](../../areas/area_nexus.md) — Nexus also uses graph-based retrieval; PPR could enhance it
- Related: [Continual Learning ATO](../../projects/project_continual_learning_ato.md) — Continual learning project could adopt non-parametric approach
- Related: [Embedding](../term_dictionary/term_embedding.md) — Dense-sparse coding combines embeddings with graph structure
- Related: [HippoRAG](../term_dictionary/term_hipporag.md) — Core subject of this paper; hippocampus-inspired RAG with KG + PPR
- Related: [PPR](../term_dictionary/term_ppr.md) — Personalized PageRank is the retrieval mechanism in HippoRAG's hippocampal index
- Related: [OpenIE](../term_dictionary/term_open_ie.md) — LLM-based OpenIE builds the open knowledge graph during offline indexing
- Related: [Catastrophic Forgetting](../term_dictionary/term_catastrophic_forgetting.md) — Primary motivation for non-parametric RAG over fine-tuning

## Questions

- Could HippoRAG 2's dense-sparse passage integration improve Nexus's retrieval quality?
- How does the PPR approach scale with graph size compared to Nexus's current traversal?
- Would the recognition memory (LLM-based triple filtering) add too much latency for production use?
- Can the OpenIE triple extraction be replaced with domain-specific KG construction?

## Related Documentation

### Paper Notes
- [paper_gutierrez2025rag_intro](paper_gutierrez2025rag_intro.md)
- [paper_gutierrez2025rag_contrib](paper_gutierrez2025rag_contrib.md)
- [paper_gutierrez2025rag_model](paper_gutierrez2025rag_model.md)
- [paper_gutierrez2025rag_exp_design](paper_gutierrez2025rag_exp_design.md)
- [paper_gutierrez2025rag_exp_result](paper_gutierrez2025rag_exp_result.md)

### Review
- [review_gutierrez2025rag](review_gutierrez2025rag.md)

### Related Literature
- [lit_lewis2020retrieval](lit_lewis2020retrieval.md) — RAG: the foundational retrieval-augmented generation paper that HippoRAG extends with graph-based knowledge integration
- [lit_edge2024local](lit_edge2024local.md) — GraphRAG: complementary graph-RAG approach using community detection + hierarchical summarization for global sensemaking queries

### Related Vault Notes
- [RAG](../term_dictionary/term_rag.md)
- [GraphRAG](../term_dictionary/term_graphrag.md)
- [Knowledge Graph](../term_dictionary/term_knowledge_graph.md)
- [Continual Learning](../term_dictionary/term_continual_learning.md)
- [KG Embeddings](../term_dictionary/term_kg_embeddings.md)
- [HippoRAG](../term_dictionary/term_hipporag.md)
- [PPR](../term_dictionary/term_ppr.md)
- [OpenIE](../term_dictionary/term_open_ie.md)
- [Catastrophic Forgetting](../term_dictionary/term_catastrophic_forgetting.md)
- [Nexus](../../areas/area_nexus.md)
- [Project Nexus](../../projects/project_nexus.md)
