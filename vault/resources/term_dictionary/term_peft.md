---
tags:
  - resource
  - terminology
  - machine_learning
  - nlp
  - fine_tuning
  - llm
  - buyer_risk_prevention
keywords:
  - PEFT
  - parameter-efficient fine-tuning
  - adapter
  - LoRA
  - prefix tuning
  - prompt tuning
  - model adaptation
  - fine-tuning
  - LLM
topics:
  - Machine Learning
  - Natural Language Processing
  - Model Adaptation
  - Fine-Tuning
language: markdown
date of note: 2026-03-04
status: active
building_block: concept
related_wiki: null
---

# PEFT - Parameter-Efficient Fine-Tuning

## Definition

Parameter-Efficient Fine-Tuning (PEFT) refers to a family of techniques that adapt large pre-trained models to downstream tasks by training only a small subset of parameters while keeping the majority of the pre-trained model frozen. Unlike traditional full fine-tuning which updates all model parameters (often billions), PEFT methods introduce a small number of trainable parameters (typically 0.01-1% of the original model size) that are sufficient to achieve comparable or superior performance. This approach dramatically reduces computational costs, memory requirements, and training time while avoiding catastrophic forgetting—the loss of previously learned knowledge during adaptation.

PEFT enables practical deployment of multiple task-specific adaptations from a single base model, as each adaptation requires storing only the small set of task-specific parameters rather than an entire model copy. This is particularly valuable for organizations like Amazon that need to maintain hundreds of specialized models across different abuse detection tasks, customer segments, and use cases.

## Context

PEFT techniques are widely adopted across Amazon for adapting foundation models to domain-specific tasks in buyer abuse prevention, customer service, and fraud detection. Within Buyer Risk Prevention (BRP), PEFT methods enable teams to fine-tune large language models for abuse detection tasks without the prohibitive costs of full model retraining. The Buyer Abuse ML team uses PEFT (particularly LoRA and QLoRA) for adapting models like Falcon-40B to buyer-seller messaging analysis, A-to-Z claim abuse detection, and threat identification.

PEFT is deployed through AWS Bedrock and SageMaker, allowing teams to maintain multiple task-specific adaptations efficiently. The approach is critical for RAG (Retrieval-Augmented Generation) systems where task-specific fine-tuning improves both retrieval relevance and generation quality. PEFT also enables rapid experimentation and iteration, as training new adapters takes hours instead of days or weeks required for full fine-tuning.

## Key Characteristics

- **Minimal Parameter Updates**: Trains only 0.01-1% of model parameters, dramatically reducing computational requirements
- **Frozen Base Model**: Original pre-trained weights remain unchanged, preserving general knowledge and preventing catastrophic forgetting
- **Multi-Task Efficiency**: Single base model supports hundreds of task-specific adapters, each requiring minimal storage
- **Comparable Performance**: Achieves performance on par with or exceeding full fine-tuning on downstream tasks
- **Fast Training**: Reduces training time from days/weeks to hours due to fewer parameters and lower memory requirements
- **Lower Memory Footprint**: Enables fine-tuning of very large models on consumer-grade hardware
- **Modular Deployment**: Adapters can be swapped dynamically at inference time for multi-task serving
- **Reduced Overfitting**: Implicit regularization from parameter constraints often improves generalization

## Performance / Metrics

- **Parameter Efficiency**: Typical PEFT methods train 0.1-1% of total parameters (e.g., 18M trainable vs 175B total for GPT-3 with LoRA)
- **Memory Reduction**: 3-10x reduction in GPU memory requirements during training compared to full fine-tuning
- **Training Speed**: 2-5x faster training time due to fewer parameters and reduced memory operations
- **Storage Efficiency**: Each task-specific adapter is 1-10% of base model size, enabling storage of 100+ adapters per base model
- **Performance Parity**: Matches or exceeds full fine-tuning on GLUE, SuperGLUE, and domain-specific benchmarks
- **QLoRA Enhancement**: Combined with quantization, achieves 75% reduction in peak GPU memory while maintaining performance

## Related Terms

- **[LoRA](term_lora.md)**: Low-Rank Adaptation - the most widely used PEFT technique, using low-rank matrix decomposition for efficient adaptation
- **[LLM](term_llm.md)**: Large Language Models - the primary type of model that PEFT techniques are designed to adapt efficiently
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation - systems that benefit from PEFT-adapted models for improved task-specific performance
- **[Transfer Learning](term_transfer_learning.md)**: The general paradigm of adapting pre-trained models, which PEFT implements in a parameter-efficient manner
- **[Hypernetwork](term_hypernetwork.md)**: Neural networks that generate weights for other networks - can be used to generate PEFT adapters dynamically
- **[Bedrock](term_bedrock.md)**: AWS service for foundation models that supports PEFT adapter deployment for custom model fine-tuning

## References

- [Supervised Fine-Tuning Wiki](https://w.amazon.com/bin/view/SMT/SelectionDiscovery/Automation/QuickSilver/Supervised-Fine-Tuning/) - Amazon internal documentation covering PEFT techniques including LoRA, QLoRA, and adapters
- [Getting Started with LLMs Guide](https://w.amazon.com/bin/view/Users/bodhwani/Quip/GettingstartedwithLLMsGuide/) - Internal guide covering PEFT techniques like LoRA and soft prompts
- [Patterns for Building LLM-based Systems](https://w.amazon.com/bin/view/Users/eugeneya/blog/llm-patterns/) - Internal wiki covering PEFT methods including adapters, LoRA, and prefix tuning
- [COAP: Context Enhanced Buyer Abuse Prevention](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_BuyerSellerMessaging/BSM_Prods_Roadmap/) - BRP project using PEFT (LoRA/QLoRA) for fine-tuning on abuse detection
- [LoRA: Low-Rank Adaptation of Large Language Models](../papers/lit_xiao2023task.md) - Research paper on LoRA, a key PEFT technique
