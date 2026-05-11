---
tags:
  - resource
  - terminology
  - machine_learning
  - llm
  - nlp
  - generative_ai
  - model_evaluation
keywords:
  - hallucination
  - confabulation
  - factual grounding
  - faithfulness
  - factuality
  - groundedness
  - LLM reliability
  - RAG
  - knowledge grounding
topics:
  - Large Language Models
  - Model Evaluation
  - Generative AI
  - NLP
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
related_wiki: null
---

# Hallucination (LLM)

## Definition

**Hallucination** in the context of Large Language Models (LLMs) refers to the generation of text that is fluent and confident but factually incorrect, unsupported by the input context, or internally inconsistent. The term is borrowed from cognitive science (where it refers to perception without external stimulus) and has become the standard label for a core failure mode of generative AI systems.

Hallucinations are categorized into two primary types:

1. **Intrinsic hallucination**: Generated content that contradicts the provided source material or context (e.g., RAG system citing a passage but misrepresenting its content)
2. **Extrinsic hallucination**: Generated content that cannot be verified from the source material — the model invents facts beyond what the context supports

The Lewis et al. (2020) RAG paper provided early evidence that retrieval-augmented generation significantly reduces hallucination: human evaluators preferred RAG's factuality 42.7% of the time vs BART's 7.1% on Jeopardy question generation.

## Why LLMs Hallucinate

### Root Causes

| Cause | Mechanism | Example |
|-------|-----------|---------|
| **Parametric knowledge gaps** | Training data doesn't cover the topic; model pattern-matches from related domains | Generating plausible but wrong dates for historical events |
| **Training distribution mismatch** | Model learned to produce fluent text, not necessarily factual text | Generating convincing-sounding but fabricated citations |
| **Exposure bias** | Autoregressive generation compounds errors — one wrong token cascades | Small factual error in early tokens leads to completely fabricated narrative |
| **Knowledge conflicts** | Multiple contradictory facts in training data; model selects the wrong one | Conflating similar entities (people, places, products) |
| **Overconfidence** | Softmax over vocabulary always produces a prediction; no "I don't know" mechanism | Answering questions about topics outside training data with false confidence |
| **Long-context degradation** | "Lost in the middle" — information in the center of long contexts is underweighted | RAG system retrieves correct passage but generator ignores it |

### The Fundamental Problem

LLMs are trained to maximize next-token probability, not factual accuracy. A fluent, common-sounding false statement may have higher token probability than an awkward but accurate one. This misalignment between training objective and desired behavior is the root of hallucination.

## Mitigation Strategies

### Retrieval-Based (RAG)

RAG is the primary mitigation strategy for hallucination in knowledge-intensive tasks:

| Strategy | How It Helps | Limitation |
|----------|-------------|------------|
| **Passage retrieval** | Grounds generation in specific source documents | Retriever may fail to find relevant passages |
| **Source attribution** | Forces model to cite retrieved passages | Model may cite passage but still confabulate |
| **Index freshness** | Knowledge updates without retraining | Only covers indexed documents |

Lewis et al. (2020) showed RAG reduces hallucination dramatically (42.7% vs 7.1% factuality preference over BART), establishing retrieval as the standard mitigation.

### Prompting-Based

- **System prompts**: "Only answer based on the provided context; say 'I don't know' otherwise"
- **Chain-of-thought**: Step-by-step reasoning reduces reasoning hallucinations
- **Few-shot examples**: Demonstrating correct behavior with sourced answers

### Training-Based

- **RLHF**: Reinforcement Learning from Human Feedback penalizes hallucinated outputs
- **Constitutional AI**: Self-critique and revision to improve factual consistency
- **DPO**: Direct Preference Optimization aligning model outputs with human preferences for factuality

### Evaluation-Based

- **Automated fact-checking**: Verify generated claims against knowledge bases
- **Self-consistency**: Multiple samples; hallucinations are typically inconsistent across samples
- **Entailment verification**: NLI models check if generation is entailed by retrieved context

## Hallucination Metrics

| Metric | Type | What It Measures |
|--------|------|-----------------|
| **FActScore** | Automatic | Fraction of atomic facts supported by a knowledge source |
| **SelfCheckGPT** | Automatic | Consistency across multiple model samples (hallucinations are inconsistent) |
| **Human factuality** | Human eval | Human judges rate factual accuracy (used in RAG paper) |
| **Groundedness** | Automatic | Whether claims are entailed by provided context |
| **Faithfulness** | Automatic | Whether summary/generation is faithful to source document |

## Context

### In Buyer Risk Prevention

Hallucination is a critical concern for LLM-based abuse detection systems:

- **GreenTEA**: SOP-driven investigation automation must not hallucinate investigation conclusions — wrong decisions directly impact customer accounts. RAG over SOPs mitigates this.
- **AskNexus**: Natural language queries over the entity graph must return factually grounded responses — hallucinated entity relationships could lead to false abuse flags
- **Abuse Slipbox Agent**: The answer-query pipeline uses graph-aware retrieval specifically to ground responses in vault source notes, with explicit citation requirements
- **Investigation Reports**: Any LLM-generated investigation summary must be verifiable against case data — hallucinated evidence details could cause regulatory issues

### The Trust Gap

For abuse prevention specifically, hallucination is not just an accuracy problem but a **trust problem**: investigators need to verify every AI-generated claim against source data. RAG with source attribution is the minimum requirement for production deployment.

## Related Terms

- **[RAG](term_rag.md)**: Retrieval-Augmented Generation — primary mitigation strategy for hallucination; grounds generation in retrieved documents
- **[LLM](term_llm.md)**: Large Language Models — the model class where hallucination is a core failure mode
- **[Fine-Tuning](term_fine_tuning.md)**: Alternative approach to reduce hallucination via domain-specific training, but doesn't eliminate it
- **[GreenTEA](term_greentea.md)**: BRP's SOP-driven investigation system that uses RAG to reduce hallucination in automation decisions
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured knowledge source that can provide factual grounding for generation
- **[Embedding](term_embedding.md)**: Dense representations enabling the semantic retrieval that RAG uses for grounding
- **[Conformal Prediction](term_conformal_prediction.md)**: Statistical framework for uncertainty quantification that could complement hallucination detection
- **[Delegated Work](term_delegated_work.md)**: In delegated workflows, hallucination compounds into silent document corruption — Laban et al. (2026) reframe hallucination as a long-horizon failure mode
- **[Critical Failure (LLM)](term_critical_failure.md)**: Single-step large-magnitude failures in long-horizon LLM use; ~80% of degradation in delegated work comes from these sparse-but-severe events

## References

### Primary Source
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../papers/lit_lewis2020retrieval.md) — Lewis et al. (2020), NeurIPS 2020. *First systematic evidence that retrieval reduces hallucination: 42.7% vs 7.1% factuality preference over parametric-only baseline.*

### Key References
- Ji, Z., et al. (2023). "Survey of Hallucination in Natural Language Generation." ACM Computing Surveys. *Comprehensive taxonomy of hallucination types, causes, and mitigations.*
- Min, S., et al. (2023). "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation." EMNLP 2023. *Standard metric for measuring hallucination at the atomic fact level.*

### Internal Documentation
- [GreenTEA](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/GreenTEA/) — BRP project using RAG to mitigate hallucination in investigation automation
