---
tags:
  - resource
  - terminology
  - context_compression
  - efficient_inference
  - prompt_compression
  - attention_mechanism
keywords:
  - gist token
  - gisting
  - context compression
  - prompt compression
  - learned compression tokens
  - soft prompt compression
  - attention mask modification
  - AutoCompressor
  - ICAE
topics:
  - Efficient Inference
  - Context Management
  - Prompt Compression
language: markdown
date of note: 2026-04-18
status: active
building_block: concept
related_wiki: null
---

# Gist Token

## Definition

A **gist token** is a special learned token that compresses prompt context into a compact latent representation within a transformer model. Unlike natural language summaries (which are human-readable text), gist tokens operate entirely in the model's embedding space — they are continuous vectors that encode the semantic content of surrounding tokens in a form the model can attend to in place of the original context. The term and method were introduced by Mu et al. (2023, NeurIPS) in "Learning to Compress Prompts with Gist Tokens."

The key innovation is that gist models can be trained with **no additional cost** over standard instruction fine-tuning by simply modifying the transformer attention mask: prompt tokens can attend to each other and to gist tokens, but generated tokens can **only** attend to gist tokens (not the original prompt). This attention bottleneck forces the model to learn to compress all necessary prompt information into the gist token representations.

## Context

Gist tokens belong to the **soft prompt compression** family of methods, which compress text into learned continuous vectors rather than shorter natural language text (hard compression). They address the problem of prompt reuse efficiency — when the same system prompt or instruction is used across many requests, encoding it repeatedly wastes both compute and KV cache memory.

The method is positioned between two extremes:
- **No compression**: Full prompt in every request (standard approach)
- **Full distillation**: Training a task-specific model that internalizes the prompt (expensive, inflexible)

Gist tokens enable a middle path: compress once, cache the gist representations, and reuse them across requests with different user inputs.

## Key Characteristics

- **Attention mask training**: No architectural changes needed — compression is learned through a modified attention mask during fine-tuning
- **Up to 26x compression**: A prompt of ~260 tokens can be compressed into ~10 gist tokens with minimal quality loss
- **Up to 40% FLOPs reduction**: Fewer tokens to attend to during generation reduces compute cost
- **Generalizable**: Once trained, a gist model can compress *unseen* prompts without additional fine-tuning
- **Cacheable**: Compressed gist representations can be cached in the KV cache and reused across requests
- **Not human-readable**: Unlike MEMENTO's natural language mementos, gist tokens are latent vectors — they cannot be inspected or debugged
- **Prompt-only compression**: Gist tokens compress input prompts, not the model's own generated output during inference
- **Requires fine-tuning**: The base model must be fine-tuned to learn gist compression — cannot be applied to frozen models (unlike ICAE)

## Taxonomy of Soft Prompt Compression Methods

| Method | Compression Target | Requires Fine-Tuning? | Decoder Compatibility | Max Input Length | Compression Ratio |
|--------|-------------------|----------------------|----------------------|-----------------|-------------------|
| **Gist Tokens** (Mu et al., 2023) | Short prompts (<30 tokens typical) | Yes (attention mask) | Fine-tuned LM only | ~260 tokens | Up to 26x |
| **AutoCompressor** (Chevalier et al., 2023) | Long contexts (up to 30K tokens) | Yes (recursive) | Fine-tuned LM only | 30,720 tokens | Variable |
| **ICAE** (Ge et al., 2024) | Long contexts (up to 512 tokens) | Encoder only (decoder frozen) | Original frozen LM | 512 tokens | 4-16x |
| **500xCompressor** (Li et al., 2024) | Very long contexts | Yes | Fine-tuned LM only | Large | Up to 500x |

## Limitations

- **Short prompt bias**: Original gist token paper primarily tested on prompts under 30 tokens — effectiveness on very long contexts is limited
- **Fine-tuning required**: Cannot be applied to a model without retraining; each base model needs its own gist-trained variant
- **Opacity**: Compressed representations cannot be inspected — if compression loses critical information, there is no way to diagnose what was lost
- **Quality degradation at high ratios**: While 26x compression is achievable, quality degrades noticeably beyond ~10x for complex instructions
- **No generation-time savings**: Gist tokens compress inputs, not the model's own chain-of-thought — they do not help with the reasoning length problem that MEMENTO addresses

## Related Terms

- **[KV Cache](term_kv_cache.md)**: Gist tokens reduce KV cache by replacing many prompt tokens with few compressed representations
- **[Attention Mechanism](term_attention_mechanism.md)**: Gist tokens modify the attention pattern — generated tokens attend only to gist representations, not the original prompt
- **[Context Engineering](term_context_engineering.md)**: Gist tokens are one approach within the broader context engineering toolkit for managing input context
- **[Block Masking](term_block_masking.md)**: Related technique from MEMENTO that physically removes KV entries; gist tokens use attention masks instead
- **[Knowledge Distillation](term_knowledge_distillation.md)**: Gist compression is conceptually related to distillation — compressing information from a larger representation into a smaller one
- **[Prompt Engineering](term_prompt_engineering.md)**: Gist tokens compress engineered prompts for efficient reuse
- **[Prompt Optimization](term_prompt_optimization.md)**: Related field — gist tokens optimize prompt representation in latent space
- **[RAG](term_rag.md)**: RAG retrieves relevant context; gist tokens compress that context for efficient processing
- **[Embedding](term_embedding.md)**: Gist tokens are learned embeddings that encode prompt semantics in continuous vector space
- **[Transformer](term_transformer.md)**: Gist tokens exploit the transformer's attention mechanism by modifying the attention mask during training
- **[vLLM](term_vllm.md)**: Serving system where cached gist representations could accelerate prompt reuse
- **[Flash Attention](term_flash_attention.md)**: Complementary efficiency technique — Flash Attention accelerates attention computation, gist tokens reduce the number of tokens to attend over

## References

- [Mu et al. (2023). "Learning to Compress Prompts with Gist Tokens." NeurIPS 2023](https://arxiv.org/abs/2304.08467)
- [Chevalier et al. (2023). "Adapting Language Models to Compress Contexts." EMNLP 2023](https://arxiv.org/abs/2305.14788)
- [Ge et al. (2024). "In-context Autoencoder for Context Compression." ICLR 2024](https://arxiv.org/abs/2307.06945)
- [Li et al. (2024). "Prompt Compression for Large Language Models: A Survey." NAACL 2025](https://arxiv.org/abs/2410.12388)
- [MEMENTO (Kontonis et al., 2026)](../papers/lit_kontonis2026memento.md) — positions MEMENTO against gist tokens; MEMENTO uses natural language summaries instead of learned vectors
