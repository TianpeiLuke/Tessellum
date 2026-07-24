---
tags:
  - resource
  - terminology
  - machine_learning
  - deep_learning
  - nlp
  - generative_ai
keywords:
  - LLM
  - Large Language Model
  - Generative AI
  - GPT
  - Claude
  - Transformer
  - NLP
  - foundation model
topics:
  - machine learning
  - natural language processing
  - automation
  - generative AI
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# LLM - Large Language Model

## Definition

**LLM** stands for **Large Language Model**. It refers to a class of deep learning models built on transformer architecture that are trained on massive text corpora (billions to trillions of tokens) to understand, generate, and reason with human language. LLMs learn statistical patterns in language during pre-training, then can be fine-tuned or prompted for specific tasks. LLMs are increasingly deployed for tasks such as classification, investigation automation, procedure-driven decision making, and agentic workflows.

**Key Function**: Enable natural language understanding, generation, and reasoning for automation of complex tasks previously requiring human intelligence.

## Full Name

**Large Language Model**

**Synonyms & Related Terms**:
- **Foundation Model**: Broader category including non-text models (e.g., DALL-E for images)
- **Generative AI (GenAI)**: AI systems that generate new content (LLMs are a subset)
- **GPT**: Generative Pre-trained Transformer (specific architecture family)
- **SLM**: Small Language Model (resource-efficient variants)

## Key Highlights

**Architecture and Training**: LLMs are built on the transformer architecture using self-attention mechanisms that capture long-range dependencies in text. They are pre-trained in a self-supervised manner on massive corpora, then adapted via supervised fine-tuning (SFT), RLHF alignment, or prompt engineering. Model scale ranges from 1B to 1T+ parameters, with emergent capabilities (in-context learning, chain-of-thought reasoning) appearing at larger scales.

**Applications and Impact**: LLMs power a broad range of automation systems, from investigation and case triage to procedure-driven decision making and document understanding. Agentic workflows that chain LLM reasoning with tools (for example via frameworks like LangGraph) extend these capabilities to multi-step tasks.

**Ecosystem and Considerations**: LLMs are deployed both as managed API services (hosting external models like Claude or GPT-4) and via custom training platforms. Key considerations include OWASP Top 10 security risks (prompt injection, data poisoning), evaluation metrics (automation rate, precision/recall), and the trade-off between capability and cost as models scale.

## Related Terms

### Core Architecture
- **[Transformer](term_transformer.md)**: Foundational architecture (self-attention, parallel processing) - basis for ALL LLMs

### ML Architecture
- **[BERT](term_bert.md)**: Bidirectional encoder model (encoder-only transformer)
- **[SBERT](term_sbert.md)**: Sentence embeddings via siamese BERT
- **[GPT](term_gpt.md)**: Generative pre-trained transformer (decoder-only)
- **[Embedding](term_embedding.md)**: Dense vector representations produced by LLMs

### Security
- **[Prompt Injection](term_prompt_injection.md)**: LLM security vulnerability
- **[RAG](term_rag.md)**: Retrieval Augmented Generation

### Frameworks
- **[PyTorch](term_pytorch.md)**: Dominant framework for LLM training and inference — all major open-source LLMs (LLaMA, Mistral, GPT-NeoX) are implemented in PyTorch

## References

### Standards & Security
- **OWASP LLM Top 10**: https://owasp.org/www-project-top-10-for-large-language-model-applications/

### External Resources
- **Attention Is All You Need (Vaswani et al., 2017)**: https://arxiv.org/abs/1706.03762
- **Language Models are Few-Shot Learners (GPT-3, Brown et al., 2020)**: https://arxiv.org/abs/2005.14165

## Summary

**LLM Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Large Language Model |
| **Architecture** | Transformer-based neural network |
| **Scale** | 1B - 1T+ parameters |
| **Training** | Self-supervised on massive text corpora |
| **Adaptation** | Fine-tuning, RLHF, prompt engineering |
| **Key Metrics** | Automation rate, AUC, precision/recall |
| **Security** | OWASP Top 10 |

**Key Insight**: LLMs represent a **paradigm shift** in automation - from hand-crafted features and rule-based systems to **natural language understanding and reasoning**. Unlike traditional ML (e.g., gradient-boosted trees) that requires extensive feature engineering, LLMs can process raw text, follow procedures expressed in natural language, and make decisions with human-like reasoning. This enables automation of the "long tail" of complex cases previously requiring human review. The key challenge is maintaining **precision and auditability** while scaling automation - addressed through techniques like structured output validation and human-in-the-loop control groups.

---

**Last Updated**: March 15, 2026
**Status**: Active - core technology for automation (2025-2026+)
</content>
</invoke>
