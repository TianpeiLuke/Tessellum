---
tags:
  - resource
  - terminology
  - quantization
  - information_theory
  - llm
  - kv_cache
keywords:
  - TurboQuant
  - vector quantization
  - data-oblivious
  - random rotation
  - scalar quantizer
  - QJL
  - KV cache
  - distortion rate
  - near-optimal
  - information-theoretic bounds
topics:
  - Quantization
  - Information Theory
  - LLM Inference Optimization
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# TurboQuant

## Definition

**TurboQuant** is a data-oblivious vector quantization algorithm (Zandieh et al., 2025) that achieves **near-optimal distortion rates** (within ~2.7× of information-theoretic lower bounds) across all bit-widths and dimensions. The key mechanism: randomly rotating input vectors induces a concentrated Beta distribution on coordinates, and the near-independence of coordinates in high dimensions allows applying optimal scalar quantizers per coordinate — reducing the hard vector quantization problem to trivial per-coordinate scalar quantization.

For inner product preservation (critical for Transformer attention), TurboQuant uses a two-stage approach: an MSE-optimal quantizer followed by a 1-bit Quantized Johnson-Lindenstrauss (QJL) correction on the residual, producing an **unbiased inner product estimator**.

## Key Properties

- **Data-oblivious**: No calibration data or codebook learning required — works on any input, suitable for streaming/online settings
- **Near-optimal**: Within ~2.7× of proven information-theoretic lower bounds on distortion rate
- **Random rotation → scalar quantization**: Reduces vector quantization to per-coordinate scalar quantization via random orthogonal rotation
- **Two-stage for inner products**: MSE quantizer + 1-bit QJL residual correction eliminates inner product bias
- **Quality-neutral at 3.5 bits**: KV cache quantization at 3.5 bits/channel shows no measurable quality degradation
- **Zero indexing time**: For nearest neighbor search, requires no codebook training — instant deployment
- **Already adopted**: ITQ3_S (3-bit LLM weight quantization) and TurboESM (protein LM KV cache) build on TurboQuant

## Applications

| Domain | Application | Key Result |
|--------|-------------|------------|
| **LLM KV cache** | Compress key-value pairs in Transformer attention | Quality-neutral at 3.5 bits (~4.6× memory reduction) |
| **Nearest neighbor search** | Compress index vectors for similarity search | Outperforms product quantization in recall with zero indexing time |
| **Protein language models** | KV cache compression for long protein sequences | 7.1× memory reduction, cosine similarity >0.96 (TurboESM) |
| **LLM weight quantization** | 3-bit weight compression with rotation-domain smoothing | Competitive with FP16 at 1.5× throughput (ITQ3_S) |

## Related Terms

- **[RaBitQ](term_rabitq.md)**: Prior art (SIGMOD 2024) using the same core technique (random rotation → per-coordinate quantization); subject of community novelty dispute
- **[ANN Search](term_ann_search.md)**: TurboQuant outperforms Product Quantization in ANN recall with zero indexing time
- **[Vector Quantization](term_vector_quantization.md)**: TurboQuant is a specific data-oblivious VQ algorithm achieving near-optimal distortion
- **[LSH](term_lsh.md)**: Hash-based ANN alternative; shares the random projection paradigm
- **[Johnson-Lindenstrauss Lemma](term_johnson_lindenstrauss_lemma.md)**: QJL (Quantized JL) is TurboQuant's residual correction for unbiased inner products
- **[Quantization](term_quantization.md)**: General concept; TurboQuant is a specific near-optimal vector quantization algorithm
- **[LLM.int8()](term_llm_int8.md)**: Prior LLM quantization method (8-bit mixed precision); TurboQuant targets lower bit-widths (2-4 bits)
- **[GPTQ](term_gptq.md)**: Data-dependent LLM quantization; TurboQuant is data-oblivious (no calibration needed)
- **[AWQ](term_awq.md)**: Activation-aware quantization; data-dependent, complementary approach
- **[LLM](term_llm.md)**: Primary application domain for KV cache compression
- **[Transformer](term_transformer.md)**: Architecture whose attention mechanism benefits from unbiased inner product quantization
- **[Scaling Law](term_scaling_law.md)**: TurboQuant enables efficient inference, complementing scaling law research

## References

### Vault Sources

- [TurboQuant Literature Note](../papers/lit_zandieh2025turboquant.md) — Full paper digest with section notes
- [TurboQuant Review](../papers/review_zandieh2025turboquant.md) — OpenReview-style evaluation (Overall 7/10)

### External Sources

- [Zandieh et al. (2025). "TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate." arXiv:2504.19874](https://arxiv.org/abs/2504.19874) — Original paper (6 citations)
