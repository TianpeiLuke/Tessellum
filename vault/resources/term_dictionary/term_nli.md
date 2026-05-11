---
tags:
  - resource
  - terminology
  - nlp
  - natural_language_inference
  - classification
keywords:
  - NLI
  - natural language inference
  - textual entailment
  - MNLI
  - DeBERTa
  - RTE
  - SNLI
  - semantic reasoning
topics:
  - Natural Language Processing
  - Semantic Analysis
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
---

# NLI — Natural Language Inference

## Definition

**Natural Language Inference (NLI)**, also called **Recognizing Textual Entailment (RTE)**, is a classification task that determines the logical relationship between a premise and a hypothesis. Given a premise P and hypothesis H, the model predicts one of three labels:

| Label | Meaning | Example (P → H) |
|-------|---------|------------------|
| **Entailment** | P logically implies H | "A dog is running" → "An animal is moving" |
| **Contradiction** | P and H are logically incompatible | "A dog is running" → "No animals are moving" |
| **Neutral** | P neither implies nor contradicts H | "A dog is running" → "A dog is brown" |

**Full Name**: Natural Language Inference / Recognizing Textual Entailment (RTE)

## Why It Matters

NLI is a foundational NLP task that serves as a proxy for **semantic understanding**. A model that can accurately determine entailment must understand:
- Lexical semantics (synonyms, hypernyms)
- Compositional semantics (negation, quantifiers)
- World knowledge (common-sense reasoning)
- Pragmatic inference

In the context of [Semantic Entropy](term_semantic_entropy.md), NLI provides the semantic equivalence oracle: [bidirectional entailment](term_bidirectional_entailment.md) (A entails B AND B entails A) defines meaning equivalence.

## Key Benchmarks

| Benchmark | Size | Characteristics |
|-----------|------|----------------|
| **SNLI** | 570K pairs | Natural images + captions; 3-way classification |
| **MNLI** (MultiNLI) | 433K pairs | Multi-genre (fiction, government, telephone, etc.); in/out-of-domain splits |
| **XNLI** | 7.5K per language | Cross-lingual NLI; 15 languages |
| **ANLI** | 163K pairs | Adversarial; human-and-model-in-the-loop |
| **RTE** | ~5K pairs | Binary (entailment vs not); part of SuperGLUE |

## Key Models

| Model | Year | MNLI Accuracy | Notes |
|-------|------|---------------|-------|
| DeBERTa-v3-large | 2021 | ~91% | Most common NLI backbone; used in Semantic Entropy |
| RoBERTa-large | 2019 | ~90% | Strong baseline; widely used for NLI |
| [BERT](term_bert.md)-large | 2019 | ~86% | First large-scale pre-trained NLI model |
| GPT-4 | 2023 | ~89% | Zero-shot; competitive but slower |

DeBERTa (Decoding-enhanced BERT with disentangled Attention) is the standard choice for NLI-dependent methods due to its strong performance and efficiency.

## Applications Beyond Entailment

- **Semantic Entropy**: NLI as bidirectional entailment oracle for meaning clustering (Kuhn et al., 2023)
- **Zero-shot classification**: NLI models can classify any text by framing as "Does [text] entail [label]?"
- **Fact verification**: Check if a claim is entailed by evidence documents
- **Summarization evaluation**: Check if a summary is faithful to the source (entailment-based faithfulness)
- **Paraphrase detection**: Bidirectional entailment ≈ paraphrase

## Related Terms

- [Semantic Entropy](term_semantic_entropy.md) — Uses NLI for bidirectional entailment clustering
- [Bidirectional Entailment](term_bidirectional_entailment.md) — The specific NLI application for meaning equivalence
- [BERT](term_bert.md) — Foundation architecture for most NLI models
- [Hallucination](term_hallucination.md) — NLI-based entailment can verify factual faithfulness
- [SBERT](term_sbert.md) — Sentence embeddings trained with NLI supervision

## References

- Bowman et al. "A large annotated corpus for learning natural language inference." EMNLP 2015. (SNLI)
- Williams et al. "A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference." NAACL 2018. (MNLI)
- He et al. "DeBERTa: Decoding-enhanced BERT with Disentangled Attention." ICLR 2021.
- [lit_kuhn2023semantic](../papers/lit_kuhn2023semantic.md) — Uses DeBERTa-based NLI for semantic entropy
