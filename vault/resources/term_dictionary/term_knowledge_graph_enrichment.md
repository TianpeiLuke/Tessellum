---
tags:
  - resource
  - terminology
  - knowledge_graph
  - information_extraction
keywords:
  - knowledge graph enrichment
  - KG enrichment
  - KG population
  - knowledge graph completion
  - KGC
topics:
  - knowledge graph construction
  - information extraction
language: markdown
date of note: 2026-04-03
status: active
building_block: concept
---

# Knowledge Graph Enrichment

## Definition

Knowledge graph enrichment is the process of adding new entities, relationships, and attributes to an existing knowledge graph from external sources (text, databases, APIs) while maintaining consistency, schema conformance, and quality. It differs from knowledge graph completion (KGC), which infers missing links from the existing graph structure alone. Enrichment involves extracting new knowledge from outside the graph and integrating it, whereas completion reasons over what is already inside.

The distinction matters: enrichment requires NER, relation extraction, and schema alignment pipelines to process external text, while completion uses embedding-based link prediction (TransE, RotatE) or rule-based reasoning over existing triples.

## Key Properties

- **External source dependency**: Enrichment requires processing unstructured or semi-structured external data (papers, web pages, databases)
- **Pipeline stages**: Typically involves ingestion → entity extraction → relation extraction → schema alignment → conflict resolution → quality assessment
- **Schema conformance**: New triples must conform to the target KG's ontology types and relation constraints
- **Conflict resolution**: New information may contradict existing KG facts, requiring temporal reasoning or confidence-based arbitration
- **Incremental nature**: Enrichment is continuous — KGs are never "complete" as new knowledge is constantly published
- **Quality-coverage tradeoff**: Aggressive enrichment increases coverage but risks introducing noise; conservative enrichment maintains quality but misses knowledge

## Taxonomy

| Approach | Method | Strengths | Limitations |
|----------|--------|-----------|-------------|
| Rule-based IE | Pattern matching, gazetteers | High precision | Low recall, brittle |
| Neural NER/RE | Supervised sequence labeling | End-to-end | Needs labeled data |
| Single-LLM | Zero-shot prompting | Flexible, no training | Hallucination, schema drift |
| Multi-agent LLM | Specialized agents with verification | High quality + coverage | Higher cost, complexity |
| Embedding-based (KGC) | TransE, RotatE, ComplEx | Scalable link prediction | Only infers from existing graph |

## Related Terms

- **[Knowledge Graph](term_knowledge_graph.md)**: The target structure being enriched
- **[NER](term_ner.md)**: Entity extraction step in the enrichment pipeline
- **[Schema Alignment](term_schema_alignment.md)**: Mapping extracted entities to KG schema types
- **[Open IE](term_open_ie.md)**: Schema-free triple extraction used as input to enrichment
- **[Ontology](term_ontology.md)**: Defines the type system that enrichment must conform to
- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Our vault's equivalent of KG entity types — classifying knowledge atoms

- **[LDA](term_lda.md)**: Topic modeling discovers latent themes in documents for KG enrichment
- **[Variational Inference](term_variational_inference.md)**: VI for latent variable models in KG embedding
- **[Exponential Family](term_exponential_family.md)**: KG embedding models often use exponential family link functions
- **[Concentration Inequality](term_concentration_inequality.md)**: KG completion error bounds use concentration theory

## References

### Vault Sources
- [KARMA (Lu et al., 2025)](../papers/lit_lu2025karma.md) — multi-agent LLM framework for automated KG enrichment
- [Enterprise KG (Kumar et al., 2025)](../papers/lit_kumar2025enterprise.md) — enterprise-focused KG construction
- [LLM-based KG Survey (Bian, 2025)](../papers/lit_bian2025llmkg.md) — comprehensive survey of LLM approaches to KG tasks

### External Sources
- [Paulheim (2017). "Knowledge Graph Refinement: A Survey of Approaches and Evaluation Methods." Semantic Web](https://content.iospress.com/articles/semantic-web/sw218)
- [ACM Survey: Automatic Knowledge Graph Construction (2023)](https://dl.acm.org/doi/10.1145/3618295)
- [Wikipedia: Knowledge graph](https://en.wikipedia.org/wiki/Knowledge_graph)
