---
tags:
  - resource
  - terminology
  - llm_serving
  - open_source
  - gpu_optimization
  - memory_management
keywords:
  - vLLM
  - LLM serving
  - PagedAttention
  - inference engine
  - KV cache management
  - continuous batching
  - copy-on-write
  - throughput optimization
topics:
  - LLM Inference Systems
  - Memory Management
  - Production ML Systems
language: markdown
date of note: 2026-03-09
status: active
building_block: concept
related_wiki: null
---

# vLLM - Virtual Large Language Model Serving Engine

## Definition

**vLLM** is an open-source, high-throughput serving engine for large language models that introduced the PagedAttention algorithm for efficient KV cache memory management. Developed at UC Berkeley by Woosuk Kwon, Ion Stoica, and collaborators, vLLM applies operating system virtual memory concepts (paging, demand allocation, copy-on-write) to GPU memory management for the attention mechanism's key-value cache.

The core innovation is storing KV cache in fixed-size, noncontiguous memory blocks mapped through a block table (analogous to OS page tables), rather than requiring contiguous pre-allocated memory. This eliminates memory fragmentation and enables on-demand allocation, reducing KV cache memory waste from 60-80% (in prior systems) to less than 4%. The result is 2-4× throughput improvement over previous state-of-the-art systems like NVIDIA FasterTransformer and Orca.

## Context

vLLM has become the de facto standard for LLM serving in both research and production environments, with 72,000+ GitHub stars and widespread adoption. It is relevant across any organization deploying LLMs at scale:

- **Open-source ecosystem**: vLLM supports most popular model architectures (LLaMA, Mistral, Qwen, GPT-NeoX, OPT, Falcon, etc.) and integrates with Hugging Face model hub
- **Production deployment**: Used by companies for real-time chat, batch inference, and API serving
- **Research platform**: Serves as the baseline serving system in most LLM systems research papers since 2023
- **Amazon context**: Relevant for any team deploying LLM-based systems (e.g., abuse detection agents, LLM classifiers) where serving throughput and cost efficiency matter. Teams using SageMaker endpoints for LLM inference may benefit from vLLM's memory management approach.

## Key Characteristics

- **PagedAttention**: Block-based KV cache management with block tables mapping logical to physical GPU memory blocks; eliminates internal and external fragmentation
- **Continuous batching**: Iteration-level scheduling that dynamically adds/removes requests from the batch at each generation step, maximizing GPU utilization
- **Copy-on-write sharing**: Shared KV cache blocks for parallel sampling, beam search, and common prefixes — reduces memory by up to 55% for beam search
- **Preemption support**: When GPU memory is exhausted, lower-priority requests can be swapped to CPU memory or recomputed later, preventing out-of-memory crashes
- **Tensor parallelism**: Supports multi-GPU serving with a centralized scheduler broadcasting block table updates to all GPU workers
- **Throughput gains**: 2-4× over FasterTransformer and Orca, with gains increasing for larger models and longer sequences
- **Block size**: Default B=16 tokens per block, providing <4% memory waste with negligible computation overhead (~5% vs. contiguous attention)

## Related Terms

- **[KV Cache](term_kv_cache.md)**: The key-value cache that vLLM manages efficiently via PagedAttention
- **[LLM](term_llm.md)**: Large language models are the workload vLLM is designed to serve
- **[Attention Mechanism](term_attention_mechanism.md)**: PagedAttention modifies how attention accesses KV cache memory
- **[Transformer](term_transformer.md)**: The model architecture whose inference vLLM optimizes
- **[Embedding](term_embedding.md)**: Input representations that are projected into the KV cache
- **[SageMaker](term_sagemaker.md)**: AWS ML platform where LLM serving (potentially via vLLM) can be deployed
- **[Foundation Model](term_foundation_model.md)**: The class of models that vLLM is designed to serve at scale
- **[Inference Scaling Law](term_inference_scaling_law.md)**: Scaling laws for inference compute, where vLLM addresses the memory bottleneck
- **[Block Masking](term_block_masking.md)**: Block masking extends vLLM's PagedAttention by enabling dynamic eviction of KV cache blocks for expired context
- **[PyTorch](term_pytorch.md)**: vLLM is built on PyTorch and uses custom CUDA kernels integrated with the PyTorch runtime for PagedAttention and continuous batching

## References

- [PagedAttention paper — Kwon et al., SOSP 2023](https://arxiv.org/abs/2309.06180)
- [vLLM GitHub Repository](https://github.com/vllm-project/vllm)
- [vLLM Documentation](https://docs.vllm.ai/)
