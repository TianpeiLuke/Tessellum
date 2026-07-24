---
tags:
  - resource
  - terminology
  - natural_language_processing
  - information_extraction
  - knowledge_graphs
keywords:
  - OpenIE
  - open information extraction
  - triple extraction
  - relation extraction
  - knowledge graph construction
topics:
  - information extraction
  - natural language processing
  - knowledge graphs
  - RAG systems
language: markdown
date of note: 2026-03-03
status: active
building_block: concept
related_wiki: null
---

# OpenIE - Open Information Extraction

## Definition
Open Information Extraction (OpenIE) is an NLP paradigm that extracts relational tuples — typically (subject, predicate, object) triples — from unstructured text without requiring a predefined schema, ontology, or target relation set. Unlike closed information extraction which targets specific relations (e.g., "works_for", "born_in"), OpenIE discovers relations directly from the text surface forms, producing a domain-independent, open-vocabulary knowledge representation. Originally introduced by the TextRunner system (2007) and refined through ReVerb, OLLIE, and Stanford CoreNLP-OpenIE, the paradigm has been transformed by LLMs which now serve as powerful zero-shot OpenIE extractors.

## Context
OpenIE is widely used for knowledge graph construction from unstructured text. Classic pipelines such as Stanford CoreNLP-OpenIE extract triples from customer utterances, documents, and web pages to bootstrap domain knowledge graphs. In the GraphRAG space, HippoRAG uses LLM-based OpenIE (e.g., Llama-3.3-70B) to extract triples during offline indexing, building the open knowledge graph that supports PPR-based retrieval. More broadly, OpenIE is relevant to entity-relationship extraction from investigation notes, documentation, and ticket-resolution workflows, where discovering relations without a predefined schema lets a system model previously unseen relationship types.

## Key Characteristics
- **Schema-Free Extraction**: No predefined relation types needed — relations are discovered from text, enabling domain-independent application
- **Triple Format**: Outputs (subject, predicate, object) tuples, directly mappable to knowledge graph edges
- **Evolution of Approaches**:
  - Rule-based: TextRunner (2007), ReVerb (2011), OLLIE (2012) — pattern matching on dependency parses
  - Neural: Supervised sequence labeling with pre-trained language models
  - LLM-based: Zero-shot or few-shot extraction using GPT-4, Claude, Llama — current state-of-the-art
- **LLM as OpenIE Extractor**: Modern systems prompt LLMs to extract structured triples, achieving higher quality than traditional pipelines but at higher computational cost
- **Noise Challenge**: OpenIE outputs are inherently noisy — redundant, incomplete, or incorrect triples require post-processing, deduplication, and validation
- **Scalability Trade-off**: Traditional OpenIE (CoreNLP) is fast but lower quality; LLM-based OpenIE is high quality but expensive at scale

## Related Terms
- **[Knowledge Graph](term_knowledge_graph.md)**: Primary consumer of OpenIE output — triples populate KG edges and nodes
- **[HippoRAG](term_hipporag.md)**: Uses LLM-based OpenIE to build the hippocampal knowledge graph index for associative retrieval
- **[NLP](term_nlp.md)**: Parent discipline encompassing OpenIE as a core information extraction task
- **[PPR](term_ppr.md)**: Personalized PageRank operates over knowledge graphs constructed via OpenIE in GraphRAG systems
- **[RAG](term_rag.md)**: GraphRAG systems use OpenIE-constructed knowledge graphs to enhance retrieval beyond vector similarity

## References
- [Banko, M. et al. (2007). *Open Information Extraction from the Web* (TextRunner). IJCAI 2007.](https://www.ijcai.org/Proceedings/07/Papers/429.pdf) — the paper that introduced the OpenIE paradigm
- [Angeli, G., Premkumar, M.J. & Manning, C.D. (2015). *Leveraging Linguistic Structure For Open Domain Information Extraction*. ACL 2015.](https://aclanthology.org/P15-1034/) — Stanford CoreNLP-OpenIE
- Source: [lit_gutierrez2025rag](../papers/lit_gutierrez2025rag.md) — first encountered in this paper
