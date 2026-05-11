---
tags:
  - resource
  - terminology
  - natural_language_processing
  - information_extraction
keywords:
  - Named Entity Recognition
  - NER
  - entity extraction
  - entity identification
  - entity chunking
  - sequence labeling
topics:
  - natural language processing
  - information extraction
language: markdown
date of note: 2026-04-03
status: active
building_block: concept
---

# Named Entity Recognition (NER)

## Definition

Named Entity Recognition (NER), also called entity identification, entity chunking, or entity extraction, is a subtask of information extraction that locates and classifies named entities in unstructured text into predefined categories such as person names (PER), organizations (ORG), locations (LOC), time expressions, quantities, and monetary values. The task is typically decomposed into two sub-problems: (1) detection of entity name spans (segmentation), and (2) classification of detected spans into entity types using a target ontology.

The term "Named Entity" was introduced at the 6th Message Understanding Conference (MUC-6) in 1996, though the task of identifying proper names in text dates to the early 1990s. NER is foundational to downstream NLP tasks including knowledge graph construction, question answering, information retrieval, and relation extraction.

## Historical Context

| Era | Period | Approach | Representative Systems |
|-----|--------|----------|----------------------|
| Rule-based | 1990s | Handcrafted patterns, gazetteers, capitalization heuristics | MUC systems |
| Statistical ML | 2000s | Feature engineering + CRF/HMM/MaxEnt decoding | Stanford NER, OpenNLP |
| Neural | 2015-2018 | BiLSTM-CRF with word embeddings | Lample et al. (2016) |
| Transformer | 2018-present | Fine-tuned BERT/RoBERTa for token classification | HuggingFace Transformers |
| LLM-based | 2023-present | Zero-shot/few-shot prompting of GPT-4, Claude, etc. | KARMA (Lu, 2025), ChatIE |

MUC-7 (1998) established the benchmark: best systems scored 93.39% F1 while human annotators scored 96-97% F1. CoNLL-2003 shared task became the standard benchmark for language-independent NER.

## Taxonomy

| Entity Type Hierarchy | Examples | Standard |
|----------------------|----------|----------|
| CoNLL (4 types) | PER, ORG, LOC, MISC | CoNLL-2003 shared task |
| BBN (29 types, 64 subtypes) | Person, Organization, GPE, Facility, etc. | BBN Technologies (2002) |
| Sekine Extended (200 subtypes) | Fine-grained: Museum, River, Disease, etc. | Sekine (2002) |
| OntoNotes (18 types) | PERSON, NORP, FAC, ORG, GPE, LOC, PRODUCT, etc. | OntoNotes 5.0 |
| Biomedical NER | Gene, Protein, Chemical, Disease, Drug | BioCreative, CHEMDNER |

## Key Properties

- **BIO/IOB tagging scheme**: Tokens labeled as B-TYPE (beginning), I-TYPE (inside), O (outside) for sequence labeling
- **Non-nested assumption**: Most NER systems assume entity spans don't overlap (though nested NER is an active research area)
- **Domain brittleness**: Systems trained on one domain (news) perform poorly on others (biomedical, social media) without adaptation
- **Evaluation via span-level F1**: A prediction must match the exact span boundaries AND entity type to count as correct (strict evaluation)
- **Gazetteer augmentation**: Entity lists (gazetteers) boost recall by providing known entity names as features
- **Low-resource challenge**: Many languages and domains lack sufficient labeled training data, driving interest in cross-lingual and few-shot NER

## Notable Systems

| System | Approach | Application |
|--------|----------|-------------|
| Stanford NER | CRF with rich features | General-purpose English NER |
| spaCy | Statistical + neural | Production NLP pipelines |
| HuggingFace Transformers | Fine-tuned BERT/RoBERTa | Token classification |
| GATE | Rule-based + ML hybrid | Multi-language, multi-domain |
| BioBERT | Domain-adapted BERT | Biomedical NER |
| KARMA EEA | LLM-based NER + embedding normalization | KG enrichment from scientific literature |

## Challenges and Limitations

- **Ambiguity**: Same name can refer to different entity types ("JFK" = person, airport, or movie)
- **Domain transfer**: Models trained on news text degrade on social media, biomedical, or legal text
- **Nested entities**: "Bank of America" contains "America" — most systems can't handle nesting
- **Fine-grained typing**: Moving from 4 types to 200+ subtypes dramatically increases annotation cost and classification difficulty
- **Noisy text**: Twitter, chat, and OCR output challenge standard NER assumptions about capitalization and grammar
- **LLM hallucination**: Zero-shot LLM-based NER can fabricate entities not present in the source text

## Related Terms

- **[Open IE](term_open_ie.md)**: Extracts (subject, predicate, object) triples without predefined schema; NER provides the entity arguments
- **[Knowledge Graph](term_knowledge_graph.md)**: Primary consumer of NER output — entities become KG nodes
- **[Ontology](term_ontology.md)**: Defines the entity type hierarchy that NER classifies into
- **[LLM](term_llm.md)**: Modern NER increasingly uses LLMs for zero-shot or few-shot entity extraction
- **[BERT](term_bert.md)**: Transformer model that revolutionized NER via fine-tuned token classification
- **[Transformer](term_transformer.md)**: Architecture underlying current state-of-the-art NER systems
- **[Embedding](term_embedding.md)**: Word/entity embeddings used for entity normalization and disambiguation

- **[Tokenization](term_tokenization.md)**: NER operates at token level — tokenizer determines entity boundaries
- **[CRF](term_crf.md)**: BiLSTM-CRF was pre-Transformer standard for NER

- **[WordPiece](term_wordpiece.md)**: WordPiece tokenization determines entity span boundaries in BERT-based NER

## References

### Vault Sources
- [KARMA (Lu et al., 2025)](../papers/lit_lu2025karma.md) — uses LLM-based NER as Entity Extraction Agent
- [KARMA Model Note](../papers/paper_lu2025karma_model.md) — details EEA agent with NER + embedding normalization

### External Sources
- [Wikipedia: Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)
- [Li et al. (2022). "A Survey on Deep Learning for NER." IEEE TKDE](https://arxiv.org/abs/2401.10825)
- [Tjong Kim Sang & De Meulder (2003). "CoNLL-2003 Shared Task." CoNLL](http://www.aclweb.org/anthology/W03-0419)
- [IBM: What Is Named Entity Recognition?](https://www.ibm.com/topics/named-entity-recognition)
