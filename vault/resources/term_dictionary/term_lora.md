---
tags:
  - resource
  - terminology
  - machine_learning
  - nlp
  - parameter_efficient_fine_tuning
  - llm
keywords:
  - LoRA
  - Low-Rank Adaptation
  - parameter-efficient fine-tuning
  - PEFT
  - adapter
  - fine-tuning
  - LLM
  - transformer
  - weight matrices
topics:
  - Machine Learning
  - Natural Language Processing
  - Model Adaptation
  - Parameter-Efficient Fine-Tuning
language: markdown
date of note: 2026-03-04
status: active
building_block: concept
related_wiki: null
---

# LoRA - Low-Rank Adaptation

## Definition

LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning (PEFT) technique that enables adaptation of large pre-trained models, particularly Large Language Models (LLMs), to specific tasks or domains without updating all model parameters. Instead of fine-tuning the entire model, LoRA injects small, trainable low-rank matrices into selected layers of the model while keeping the original pre-trained weights frozen. This approach dramatically reduces the number of trainable parameters (by up to 10,000x) and GPU memory requirements (by up to 3x) while maintaining or even improving performance compared to full fine-tuning.

The core insight behind LoRA is that weight updates during adaptation have low "intrinsic rank" - meaning the changes needed to adapt a model can be represented efficiently using low-dimensional matrices. For a pre-trained weight matrix W, LoRA represents the update as W' = W + BA, where B and A are small trainable matrices with much lower rank than W. During inference, the LoRA adapter can be merged with the base model or swapped dynamically, enabling efficient multi-task deployment.

## Context

LoRA is widely used to adapt foundation models to domain-specific tasks such as classification, retrieval, and dialogue, without the computational overhead of full model retraining. The technique is particularly valuable for RAG (Retrieval-Augmented Generation) systems where task-specific adaptation improves retrieval relevance and generation quality.

LoRA adapters are commonly deployed in production through managed model-hosting platforms, allowing teams to maintain multiple task-specific adaptations of a single base model. Combining LoRA with quantization techniques (QLoRA) further reduces the memory footprint for large-scale deployment.

## Key Characteristics

- **Low-Rank Decomposition**: Represents weight updates as the product of two small matrices (rank r << d, where d is the original dimension), dramatically reducing trainable parameters
- **Frozen Base Model**: Original pre-trained weights remain unchanged, preserving general knowledge and preventing catastrophic forgetting
- **Task-Specific Adapters**: Each task gets its own small adapter (typically 1-10% of base model size), enabling efficient multi-task deployment
- **Inference Flexibility**: Adapters can be merged with base weights for no-overhead inference, or swapped dynamically for multi-task serving
- **Implicit Regularization**: The low-rank constraint provides regularization, often outperforming full fine-tuning and reducing overfitting
- **Layer Selection**: Typically applied to attention layers (query, value projections) in transformers, though can be applied to any weight matrix
- **Rank Tuning**: Hyperparameter r (rank) controls the trade-off between adaptation capacity and parameter efficiency (typical values: 4-64)
- **Compatibility**: Works with quantized models (QLoRA), enabling fine-tuning of very large models on consumer hardware

## Performance / Metrics

- **Parameter Reduction**: Reduces trainable parameters by 10,000x compared to full fine-tuning (e.g., GPT-3 175B → 18M trainable parameters with rank 4)
- **Memory Efficiency**: Reduces GPU memory requirements by 3x during training, enabling fine-tuning on smaller instances
- **QLoRA Enhancement**: Combined with 4-bit quantization, achieves 75% reduction in peak GPU memory usage while maintaining comparable performance
- **Inference Overhead**: Zero overhead when adapter is merged; minimal overhead (<5%) for dynamic adapter swapping
- **Performance**: Matches or exceeds full fine-tuning performance on downstream tasks (GLUE, SuperGLUE benchmarks)
- **Adapter Size**: Typical LoRA adapter is 1-10% of base model size, enabling storage of hundreds of task-specific adapters

## Related Terms

- **[PEFT](term_peft.md)**: Parameter-Efficient Fine-Tuning - the broader family of techniques that LoRA belongs to, including adapters, prefix tuning, and prompt tuning
- **[LLM](term_llm.md)**: Large Language Models - the primary type of model that LoRA is used to adapt, including models like GPT, Falcon, and Claude
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation - systems that combine retrieval with generation, often using LoRA-adapted models for improved task-specific performance
- **[Hypernetwork](term_hypernetwork.md)**: Neural networks that generate weights for other networks - HyperLoRA extends this concept to generate LoRA adapters conditioned on task features
- **[Transfer Learning](term_transfer_learning.md)**: The general paradigm of adapting pre-trained models to new tasks, which LoRA implements in a parameter-efficient manner
- **[Intrinsic Dimensionality](term_intrinsic_dimensionality.md)**: Theoretical foundation for LoRA — weight updates during adaptation have low intrinsic rank, justifying the low-rank constraint
- **[Dimensionality Reduction](term_dimensionality_reduction.md)**: LoRA is a form of dimensionality reduction for weight updates — projecting full-rank updates to low-rank subspace
- **[PCA](term_pca.md)**: PCA and LoRA both exploit low-rank structure; PCA in data space, LoRA in weight update space
- **[QLoRA](term_qlora.md)**: Extension combining 4-bit quantization of base model with 16-bit LoRA adapters, enabling 65B fine-tuning on a single GPU

## References

### Primary Source
- [LoRA: Low-Rank Adaptation of Large Language Models](../papers/lit_hu2021lora.md) — Hu et al. (2021), ICLR 2022. arXiv:2106.09685. *Foundational paper: W = W₀ + BA formulation, 10,000× parameter reduction, zero inference latency, applied to GPT-3 175B.*

### Extensions
- [Task-Agnostic Low-Rank Adapters for Unseen English Dialects](../papers/lit_xiao2023task.md) — Xiao et al. (2023), EMNLP. *HyperLoRA: extends LoRA with hypernetworks for zero-shot dialect adaptation.*

### External Resources
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) — Dettmers et al. (2023). 4-bit quantization of the base model with LoRA adapters.
- [Hugging Face PEFT documentation](https://huggingface.co/docs/peft) — reference implementation of LoRA, QLoRA, and related PEFT techniques.
