---
tags:
  - resource
  - terminology
  - quantization
  - vector_quantization
  - nearest_neighbor
  - randomized_algorithms
keywords:
  - RaBitQ
  - Randomized Bit Quantization
  - vector quantization
  - random rotation
  - sign quantization
  - unbiased estimator
  - ANN search
  - Product Quantization
  - theoretical error bound
topics:
  - Vector Quantization
  - Approximate Nearest Neighbor Search
  - Randomized Algorithms
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# RaBitQ (Randomized Bit Quantization)

## Definition

**RaBitQ (Randomized Bit Quantization)** is a vector quantization method (Gao & Long, SIGMOD 2024) that compresses D-dimensional vectors into **D-bit strings** (1 bit per dimension) with sharp theoretical error bounds for approximate nearest neighbor (ANN) search. The key mechanism: applying a random orthogonal rotation to a bi-valued codebook (±1/√D), then storing the signs of each data vector's inverse-rotated coordinates as the binary code. An unbiased ratio estimator ($\langle \bar{o}, q \rangle / \langle \bar{o}, o \rangle$) corrects for quantization distortion, achieving O(1/√D) error that matches information-theoretic lower bounds.

RaBitQ is the **first vector quantization method for ANN search with formal error bounds**, outperforming Product Quantization (PQ) with half the code length while remaining robust on datasets where PQ catastrophically fails. It is also the prior work at the center of the **TurboQuant novelty dispute** — TurboQuant (2025) uses the same core technique (random rotation → per-coordinate quantization) extended to multi-bit settings.

## Key Properties

- **1 bit per dimension**: D-dimensional vectors → D-bit binary codes — minimal representation with near-optimal error
- **Theoretical error bound**: $O(1/\sqrt{D})$ absolute error with exponentially decaying failure probability — first formal guarantee for VQ in ANN search
- **Unbiased ratio estimator**: Uses $\langle \bar{o}, q \rangle / \langle \bar{o}, o \rangle$ instead of raw inner product to correct quantization bias
- **Data-oblivious**: No calibration data or codebook learning — random rotation provides uniform coverage
- **Bitwise efficient**: D-bit codes enable XOR + popcount distance computation (~3× faster than PQ per operation)
- **Robust**: Maintains high recall on all datasets, including MSong where PQ drops below 60%
- **Priority over TurboQuant**: Published at SIGMOD 2024 (May 2024), predating TurboQuant (April 2025)

## Algorithm

| Step | Operation | Purpose |
|------|-----------|---------|
| 1. Normalize | $o = (o_r - c) / \|o_r - c\|$ | Map to unit sphere |
| 2. Inverse rotate | $o' = P^{-1} \cdot o$ | Apply random rotation |
| 3. Sign quantize | $b_i = \text{sign}(o'_i)$ | 1-bit per coordinate |
| 4. Store | D-bit string $b$ + scalar $\|o_r - c\|$ | Compact representation |
| 5. Query | XOR + popcount for $\langle \bar{o}, q \rangle$ | Bitwise distance |
| 6. Estimate | $\hat{\langle o, q \rangle} = \langle \bar{o}, q \rangle / \langle \bar{o}, o \rangle$ | Unbiased correction |

## The TurboQuant Dispute

RaBitQ's relationship to TurboQuant (Zandieh et al., 2025) is the subject of a community dispute:
- **Shared core technique**: Both use random rotation → per-coordinate quantization → unbiased inner product estimation
- **TurboQuant extends**: Multi-bit quantization (2-4 bits), Beta distribution analysis, QJL correction, KV cache application
- **Dispute**: TurboQuant initially characterized RaBitQ's bounds as "suboptimal" (later retracted); community found TurboQuant's response "disingenuous" (Reddit, 133 upvotes)
- See [TurboQuant Review](../papers/review_zandieh2025turboquant.md) for full dispute documentation

## Related Terms

- **[TurboQuant](term_turboquant.md)**: Extends RaBitQ's core technique to multi-bit KV cache quantization; subject of novelty dispute
- **[ANN Search](term_ann_search.md)**: RaBitQ is a quantization-based ANN method with formal error bounds
- **[Vector Quantization](term_vector_quantization.md)**: RaBitQ is a specific randomized VQ algorithm (1 bit/dim)
- **[LSH](term_lsh.md)**: Hash-based ANN alternative; both use randomization but LSH produces hash buckets while RaBitQ produces distance estimates
- **[Johnson-Lindenstrauss Lemma](term_johnson_lindenstrauss_lemma.md)**: JL underpins random rotation techniques; RaBitQ's orthogonal rotation is JL-related
- **[Quantization](term_quantization.md)**: General quantization concepts; RaBitQ is a specific vector quantization algorithm
- **[GPTQ](term_gptq.md)**: Data-dependent LLM quantization (contrast with RaBitQ's data-oblivious approach)
- **[LLM.int8()](term_llm_int8.md)**: Mixed-precision LLM quantization; different approach
- **[LLM](term_llm.md)**: Downstream application (KV cache quantization via RaBitQ's technique)
- **[Transformer](term_transformer.md)**: Architecture whose attention mechanism benefits from unbiased inner product quantization

## References

### Vault Sources

- [RaBitQ Literature Note](../papers/lit_gao2024rabitq.md) — Full paper digest with section notes
- [RaBitQ Review](../papers/review_gao2024rabitq.md) — OpenReview-style evaluation (Overall 8/10)
- [TurboQuant Review](../papers/review_zandieh2025turboquant.md) — Documents the RaBitQ vs TurboQuant dispute

### External Sources

- [Gao & Long (2024). "RaBitQ: Quantizing High-Dimensional Vectors with a Theoretical Error Bound for ANN Search." SIGMOD](https://arxiv.org/abs/2405.12497) — Original paper (58 citations)
- [OpenReview Discussion](https://openreview.net/forum?id=tO3ASKZlok) — TurboQuant review thread documenting the dispute
