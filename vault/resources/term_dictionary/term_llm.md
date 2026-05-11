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
  - buyer risk prevention
  - machine learning
  - natural language processing
  - automation
  - generative AI
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/AWS_Proactive_Security/Guidebook/LLM_GenAI_Security/Introduction/
---

# LLM - Large Language Model

## Definition

**LLM** stands for **Large Language Model**. It refers to a class of deep learning models built on transformer architecture that are trained on massive text corpora (billions to trillions of tokens) to understand, generate, and reason with human language. LLMs learn statistical patterns in language during pre-training, then can be fine-tuned or prompted for specific tasks. At Amazon/BRP, LLMs are increasingly deployed for abuse detection, investigation automation, SOP-driven decision making, and agentic workflows.

**Key Function**: Enable natural language understanding, generation, and reasoning for automation of complex tasks previously requiring human intelligence.

## Full Name

**Large Language Model**

**Synonyms & Related Terms**:
- **Foundation Model**: Broader category including non-text models (e.g., DALL-E for images)
- **Generative AI (GenAI)**: AI systems that generate new content (LLMs are a subset)
- **GPT**: Generative Pre-trained Transformer (specific architecture family)
- **SLM**: Small Language Model (resource-efficient variants like LILA)

## Key Highlights

**Architecture and Training**: LLMs are built on the transformer architecture using self-attention mechanisms that capture long-range dependencies in text. They are pre-trained in a self-supervised manner on massive corpora, then adapted via supervised fine-tuning (SFT), RLHF alignment, or prompt engineering. Model scale ranges from 1B to 1T+ parameters, with emergent capabilities (in-context learning, chain-of-thought reasoning) appearing at larger scales. See [thought_llm_architecture](../analysis_thoughts/thought_llm_architecture.md) for full details.

**BRP Applications and Impact**: LLMs power major BRP automation systems including AutoSignality (AUC 0.854, $2.05MM savings), GreenTEA (PFW automation 15% to 50%), SOPA (98.9% accuracy, 98% automation rate), and Abuse Polygraph ($100K weekly savings). Agentic workflows using LangGraph-based investigation agents are in development. See [thought_llm_brp_applications](../analysis_thoughts/thought_llm_brp_applications.md) for all application details.

**Ecosystem and Considerations**: Amazon deploys LLMs via Bedrock (external models like Claude, GPT-4) and SageMaker (custom training), with internal models including LILA and Nova. Key considerations include OWASP Top 10 security risks (prompt injection, data poisoning), evaluation metrics (automation rate, LPA, precision/recall), and a roadmap toward BRP-native foundation models by 2027+. See [thought_llm_security](../analysis_thoughts/thought_llm_security.md), [thought_llm_evaluation_metrics](../analysis_thoughts/thought_llm_evaluation_metrics.md), and [thought_llm_evolution_roadmap](../analysis_thoughts/thought_llm_evolution_roadmap.md) for details.

## See Also

- [How LLMs Work - Architecture and Key Concepts](../analysis_thoughts/thought_llm_architecture.md)
- [LLM Models at Amazon](../analysis_thoughts/thought_llm_models_at_amazon.md)
- [LLM BRP Applications](../analysis_thoughts/thought_llm_brp_applications.md)
- [LLM Technical Considerations - Prompting, RAG, and Fine-Tuning](../analysis_thoughts/thought_llm_techniques.md)
- [LLM Security Considerations](../analysis_thoughts/thought_llm_security.md)
- [LLM Evaluation Metrics](../analysis_thoughts/thought_llm_evaluation_metrics.md)
- [LLM Infrastructure at Amazon](../analysis_thoughts/thought_llm_infrastructure.md)
- [LLM Evolution and BRP Roadmap](../analysis_thoughts/thought_llm_evolution_roadmap.md)

## Related Terms

### Core Architecture
- **[Transformer](term_transformer.md)**: Foundational architecture (self-attention, parallel processing) - basis for ALL LLMs

### ML Architecture
- **[BERT](term_bert.md)**: Bidirectional encoder model (encoder-only transformer)
- **[SBERT](term_sbert.md)**: Sentence embeddings via siamese BERT
- **[GPT](term_gpt.md)**: Generative pre-trained transformer (decoder-only)
- **[Embedding](term_embedding.md)**: Dense vector representations produced by LLMs

### BRP Applications
- **[GreenTEA](term_greentea.md)**: SOP-to-LLM automation framework
- **[AutoSignality](term_autosignality.md)**: LLM-powered investigation automation
- **[SOPA](term_sopa.md)**: SOP-Aware LLM for BRW
- **[DeepCARE](term_deepcare.md)**: Embedding-based automation (LLM augmentation target)

### Amazon Infrastructure
- **[LILA](term_lila.md)**: Small Language Model for behavior understanding
- **[SessionMiner](term_sessionminer.md)**: GPT-2 for traffic stream analysis
- **[Bedrock](term_bedrock.md)**: Managed LLM service

### Security
- **[Prompt Injection](term_prompt_injection.md)**: LLM security vulnerability
- **[RAG](term_rag.md)**: Retrieval Augmented Generation

### Frameworks
- **[PyTorch](term_pytorch.md)**: Dominant framework for LLM training and inference — all major open-source LLMs (LLaMA, Mistral, GPT-NeoX) are implemented in PyTorch

## References

### Amazon Documentation
- **LLM Security Guidebook**: https://w.amazon.com/bin/view/AWS_Proactive_Security/Guidebook/LLM_GenAI_Security/
- **GenAI Policy**: https://policy.a2z.com/docs/568686/publication
- **OWASP LLM Top 10**: https://owasp.org/www-project-top-10-for-large-language-model-applications/

### Science Domain
- **Large Language Models Wiki**: https://w.amazon.com/bin/view/Science-domain-talent-maps/llm/
- **Alexa AI LLM**: https://w.amazon.com/bin/view/AlexaAI/LargeLanguageModels/

### AWS Resources
- **Amazon Bedrock**: https://aws.amazon.com/bedrock/
- **SageMaker LLM**: https://docs.aws.amazon.com/sagemaker/latest/dg/large-language-models.html

## Summary

**LLM Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Large Language Model |
| **Architecture** | Transformer-based neural network |
| **Scale** | 1B - 1T+ parameters |
| **Training** | Self-supervised on massive text corpora |
| **Adaptation** | Fine-tuning, RLHF, prompt engineering |
| **BRP Applications** | GreenTEA, AutoSignality, SOPA, Abuse Polygraph |
| **Amazon Models** | LILA (internal), Claude/GPT-4/Titan (Bedrock) |
| **Key Metrics** | Automation rate, LPA, AUC, precision/recall |
| **Infrastructure** | Bedrock, SageMaker, AMES |
| **Security** | OWASP Top 10, Amazon GenAI Policy |

**Key Insight**: LLMs represent a **paradigm shift** in BRP automation - from hand-crafted features and rule-based systems to **natural language understanding and reasoning**. Unlike traditional ML (XGBoost, DeepCARE) that requires extensive feature engineering, LLMs can process raw investigation data (Paragon/Nautilus), follow SOPs expressed in natural language, and make decisions with human-like reasoning. This enables automation of the "long tail" of complex cases previously requiring human investigators. The key challenge is maintaining **precision and auditability** while scaling automation - addressed through techniques like Chain-of-SOPs (GreenTEA), structured output validation, and human-in-the-loop control groups.

---

**Last Updated**: March 15, 2026
**Status**: Active - core technology for BRP automation (2025-2026+)
