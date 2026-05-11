---
tags:
- resource
- terminology
keywords:
- CDK
- Centralized Documented Knowledge
- knowledge base
- document store
- vector store
- knowledge graph
- BRP
- agentic AI
topics:
- terminology
- knowledge management
language: markdown
date of note: 2026-04-07
status: active
building_block: concept
---

# CDK — BRP Centralized Documented Knowledge

**CDK (Centralized Documented Knowledge)** is a proposed shared control plane for ingesting, standardizing, and governing documented knowledge across all BRP pillars. Instead of each team building and maintaining its own knowledge stores, CDK serves as a unified infrastructure with consistent metadata and clear ownership.

## Architecture

CDK separates the control plane from the serving layer:
- **Control plane (CDK)**: Full authoritative corpus with unified metadata (domain, ownership, permissions, canonical identifiers)
- **Serving layer**: Agent-specific tools act as scoped low-latency views derived from CDK
- LLM agents primarily operate on curated subsets; query CDK directly only for cross-domain knowledge

## Hybrid Knowledge Strategy

BRP requires three complementary storage types:

| Store Type | Purpose | When to Use |
|-----------|---------|-------------|
| **Document stores** | Internal and business knowledge | Root causing via Q&A in natural language |
| **Vector stores** | Data prepared as ML model inputs | Comparing similarity of known entities |
| **Knowledge graphs** | Multi-modality data as knowledge | Discovering unknown relations between disconnected attributes |

## Current Status

- PR building prototype during PRE hackathon (ETA 04/30)
- PRFAQ draft being discussed across BRP
- PR partnering with BAP to evaluate graph stores (Slipbox)

## Related Terms

- [Slipbox](term_slipbox.md) — BAP's graph-based knowledge system (evaluated by PR)
- [Knowledge Graph](term_knowledge_graph.md) — Graph-based knowledge representation
- [RAG](term_rag.md) — Retrieval-Augmented Generation

## Related Terms (additional)

- [AIDE](../../projects/aides/project_aides.md) — Agentic AI tool that would consume CDK
- [MIDAS](term_midas.md) — Model migration that benefits from documented knowledge
- **[BuilderHub Create](term_builderhub_create.md)**: Application creation portal using CDK templates
- **[SAM CLI](term_sam_cli.md)**: Local testing tool for Lambda CDK applications
- **[BONES CLI](term_bones_cli.md)**: Legacy scaffolding CLI for CDK applications

## References

- [BRP Science QTR Q1 2026 — FAQs & Goals](../documentation/mtr/qtr_brp_qtr_2026_q1_faq_goals.md)
