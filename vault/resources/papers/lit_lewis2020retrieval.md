---
tags:
  - resource
  - literature_note
  - information_retrieval
  - nlp
  - knowledge_intensive
  - generative_ai
keywords:
  - RAG
  - retrieval-augmented generation
  - parametric memory
  - non-parametric memory
  - Dense Passage Retrieval
  - DPR
  - BART
  - knowledge-intensive NLP
  - open-domain QA
  - latent variable model
  - marginalization
  - index hot-swapping
topics:
  - Information Retrieval
  - NLP
  - Knowledge-Intensive Tasks
  - Language Generation
  - Generative AI
domain: "Retrieval-Augmented Generation"
language: markdown
date of note: 2026-03-08
paper_title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
authors:
  - Patrick Lewis
  - Ethan Perez
  - Aleksandra Piktus
  - Fabio Petroni
  - Vladimir Karpukhin
  - Naman Goyal
  - Heinrich Küttler
  - Mike Lewis
  - Wen-tau Yih
  - Tim Rocktäschel
  - Sebastian Riedel
  - Douwe Kiela
year: 2020
source: "arXiv:2005.11401"
venue: "NeurIPS 2020"
DOI: ""
arXiv: "2005.11401"
semantic_scholar_id: "659bf9ce7175e1ec266ff54359e2bd76e0b7ff31"
zotero_key: "H52TZPYL"
paper_id: lewis2020retrieval
paper_notes:
  - paper_lewis2020retrieval_intro.md
  - paper_lewis2020retrieval_contrib.md
  - paper_lewis2020retrieval_model.md
  - paper_lewis2020retrieval_exp_design.md
  - paper_lewis2020retrieval_exp_result.md
status: active
building_block: hypothesis
---

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks |
| **Authors** | Lewis, Perez, Piktus, Petroni, Karpukhin, Goyal, Küttler, Lewis, Yih, Rocktäschel, Riedel, Kiela (12 authors) |
| **Year** | 2020 (NeurIPS 2020) |
| **Venue** | NeurIPS 2020 |
| **arXiv** | [2005.11401](https://arxiv.org/abs/2005.11401) |
| **S2 ID** | 659bf9ce7175e1ec266ff54359e2bd76e0b7ff31 |
| **Zotero** | H52TZPYL |
| **Citations** | 11,802 |

## Abstract

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_lewis2020retrieval_intro](paper_lewis2020retrieval_intro.md) | LLM knowledge limitations; parametric vs non-parametric memory; gap in retrieval for generation; prior work (REALM, DPR, kNN-LM) |
| **Contribution** | [paper_lewis2020retrieval_contrib](paper_lewis2020retrieval_contrib.md) | 4 contributions: general-purpose RAG architecture, RAG-Sequence vs RAG-Token formulations, SOTA on 3 QA benchmarks, index hot-swapping |
| **Model** | [paper_lewis2020retrieval_model](paper_lewis2020retrieval_model.md) | DPR retriever (bi-encoder BERT) + BART generator; p(y|x) = Σ p(z|x)p(y|x,z) marginalization; FAISS MIPS over 21M Wikipedia passages; 516M trainable params |
| **Experiment Design** | [paper_lewis2020retrieval_exp_design](paper_lewis2020retrieval_exp_design.md) | 4 task categories, 7 datasets (NQ, TriviaQA, WQ, CT, MS-MARCO, Jeopardy, FEVER); 6 baselines (T5-11B, REALM, DPR) |
| **Experiment Results** | [paper_lewis2020retrieval_exp_result](paper_lewis2020retrieval_exp_result.md) | SOTA on NQ (44.5), WQ (45.5), CT (52.2); factuality 42.7% vs BART 7.1%; diversity 83.5% vs 70.7%; index hot-swapping works; learned retrieval +4 EM over BM25 |
| **Review** | [review_lewis2020retrieval](review_lewis2020retrieval.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY -->

**Introduction**: Pre-trained language models store factual knowledge in parameters but struggle with knowledge access, currency, and provenance on knowledge-intensive tasks. Prior retrieval-augmented models (REALM, DPR) were limited to extractive tasks. No general-purpose architecture existed for combining retrieval with sequence-to-sequence generation.

**Contribution**: RAG introduces the first hybrid architecture combining pre-trained parametric memory (BART-large) with non-parametric memory (dense Wikipedia index via DPR) for generation. Two formulations — RAG-Sequence (same document for whole sequence) and RAG-Token (different document per token) — treat retrieved documents as latent variables marginalized during generation. Index hot-swapping enables knowledge updates without retraining.

**Model**: The retriever uses DPR bi-encoder ($\text{BERT}_{\text{BASE}}$) computing $p_\eta(z|x) \propto \exp(\mathbf{d}(z)^\top \mathbf{q}(x))$ over 21M Wikipedia passages indexed in FAISS. The generator (BART-large, 406M params) processes concatenated [input; retrieved_passage] and generates output. RAG-Sequence marginalizes at sequence level; RAG-Token at token level. Document encoder is frozen; query encoder and BART are fine-tuned end-to-end.

**Results**: RAG sets new SOTA on Natural Questions (44.5 EM, +4 over REALM), WebQuestions (45.5), and CuratedTrec (52.2), outperforming T5-11B (20× more parameters). On Jeopardy question generation, human evaluators prefer RAG's factuality 42.7% vs BART's 7.1%. RAG generates more diverse text (83.5% vs 70.7% distinct trigrams). Index hot-swapping from Wikipedia 2016→2018 updates world knowledge without retraining.

## Relevance to Our Work

- [RAG](../term_dictionary/term_rag.md) — The foundational technique this paper introduces; used extensively in BRP for GreenTEA, AskNexus, DeepCARE, and Abuse Slipbox
- [LLM](../term_dictionary/term_llm.md) — Large Language Models whose knowledge limitations RAG addresses
- [Embedding](../term_dictionary/term_embedding.md) — Dense vector representations enabling the DPR retrieval component
- [FAISS](../term_dictionary/term_faiss.md) — Facebook AI Similarity Search used for efficient MIPS in RAG's retriever
- [Vector Database](../term_dictionary/term_vector_database.md) — The FAISS index serves as a vector database for 21M passage vectors
- [Knowledge Graph](../term_dictionary/term_knowledge_graph.md) — Alternative non-parametric memory structure; Graph-RAG extends flat retrieval to structured graphs
- [Fine-Tuning](../term_dictionary/term_fine_tuning.md) — RAG fine-tunes retriever + generator jointly; represents an alternative adaptation strategy to full fine-tuning or LoRA
- [Transformer](../term_dictionary/term_transformer.md) — Architecture underlying both retriever (BERT) and generator (BART)

## Related Documentation

### Paper Notes
- [paper_lewis2020retrieval_intro](paper_lewis2020retrieval_intro.md)
- [paper_lewis2020retrieval_contrib](paper_lewis2020retrieval_contrib.md)
- [paper_lewis2020retrieval_model](paper_lewis2020retrieval_model.md)
- [paper_lewis2020retrieval_exp_design](paper_lewis2020retrieval_exp_design.md)
- [paper_lewis2020retrieval_exp_result](paper_lewis2020retrieval_exp_result.md)

### Related Vault Notes
- [RAG](../term_dictionary/term_rag.md)
- [LLM](../term_dictionary/term_llm.md)
- [Embedding](../term_dictionary/term_embedding.md)
- [FAISS](../term_dictionary/term_faiss.md)
- [Vector Database](../term_dictionary/term_vector_database.md)
- [Knowledge Graph](../term_dictionary/term_knowledge_graph.md)
- [Transformer](../term_dictionary/term_transformer.md)
- [Fine-Tuning](../term_dictionary/term_fine_tuning.md)
- [Attention Mechanism](../term_dictionary/term_attention_mechanism.md)

### Related Literature
- [From RAG to Memory (Gutierrez et al., 2025)](lit_gutierrez2025rag.md) — Survey tracing RAG's evolution from this foundational paper to modern memory-augmented systems
- [LoRA (Hu et al., 2021)](lit_hu2021lora.md) — Alternative adaptation strategy (parameter-efficient fine-tuning) vs RAG's retrieval-based approach
- [Attention Is All You Need (Vaswani et al., 2017)](lit_vaswani2017attention.md) — Transformer architecture underlying both retriever and generator
- [BERT (Devlin et al., 2019)](lit_devlin2019bert.md) — Pre-trained encoder model used as DPR retriever backbone
- [Scaling Laws (Kaplan et al., 2020)](lit_kaplan2020scaling.md) — RAG challenges pure scaling by achieving comparable results with 20× fewer parameters
