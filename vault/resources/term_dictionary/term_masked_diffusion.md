---
tags:
  - resource
  - terminology
  - deep_learning
  - generative_model
  - self_supervised_learning
keywords:
  - masked diffusion
  - discrete diffusion
  - D3PM
  - MaskGIT
  - MDLM
  - absorbing diffusion
  - multinomial diffusion
  - discrete denoising
  - masked generative model
  - corrupt-then-reconstruct
topics:
  - Deep Learning
  - Generative Models
  - Self-Supervised Learning
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Masked Diffusion

## Definition

**Masked diffusion** is a family of generative models that unify the **discrete masking** paradigm from [Masked Language Models](term_mlm.md) with the **iterative denoising** framework from [Diffusion Models](term_diffusion_model.md). Instead of adding continuous Gaussian noise (as in DDPM), masked diffusion defines a forward corruption process that progressively replaces tokens or patches with a `[MASK]` absorbing state. The reverse process learns to predict the original content at masked positions, iteratively unmasking over multiple steps to generate samples from pure mask tokens.

This bridges a structural gap in the vault: [MLM](term_mlm.md) and [Diffusion Model](term_diffusion_model.md) both implement the corrupt-then-reconstruct paradigm (see [Thought: Corrupt-Then-Reconstruct](../analysis_thoughts/thought_corrupt_then_reconstruct_bert_ddpm.md)) but were developed independently in different communities (NLP vs. computer vision). Masked diffusion models formalize the connection and show that discrete masking can be treated as a special case of the diffusion framework.

## Full Name

Masked Diffusion Model (also: Discrete Denoising Diffusion, Absorbing Diffusion)

## Also Known As

- Discrete Diffusion
- Absorbing-state Diffusion
- Masked Generative Model (when framed without explicit diffusion formalism)

## Core Idea

### Forward Process (Corruption)

In continuous diffusion (DDPM), the forward process adds Gaussian noise: $q(\mathbf{x}_t | \mathbf{x}_{t-1})$ is a Gaussian transition. In masked diffusion, the forward process is a **discrete Markov chain** where each token transitions to a `[MASK]` absorbing state with probability $\beta_t$ at each step:

$$q(x_t = \texttt{[MASK]} \mid x_{t-1} = v) = \beta_t, \quad q(x_t = v \mid x_{t-1} = v) = 1 - \beta_t$$

After $T$ steps, all tokens are masked ($x_T = \texttt{[MASK]}$ everywhere), analogous to how continuous diffusion converges to pure Gaussian noise.

### Reverse Process (Generation)

The reverse process predicts which tokens to unmask and what values to assign them. At each step $t$, the model:
1. Takes partially masked input $\mathbf{x}_t$
2. Predicts $p_\theta(x_0 | \mathbf{x}_t)$ — the original token at each masked position
3. Unmasks a subset of positions based on confidence

Generation starts from fully masked $\mathbf{x}_T$ and iteratively unmasks until $\mathbf{x}_0$ is recovered.

### Connection to DDPM and MLM

| Dimension | MLM (BERT) | DDPM | Masked Diffusion |
|-----------|-----------|------|------------------|
| **Corruption** | Fixed 15% random masking | Continuous Gaussian noise over $T$ steps | Progressive masking over $T$ steps |
| **Corruption space** | Discrete (token → [MASK]) | Continuous ($\mathbf{x} + \boldsymbol{\epsilon}$) | Discrete (token → [MASK]) |
| **Training** | Single corruption level | All corruption levels (sample $t$ uniformly) | All corruption levels (sample $t$ uniformly) |
| **Prediction target** | Original token | Noise $\boldsymbol{\epsilon}$ | Original token (or transition probability) |
| **Generation** | Not designed for generation | Iterative denoising ($T$ steps) | Iterative unmasking ($T$ steps) |
| **Purpose** | Representation learning | Generative modeling | Generative modeling (+ representations) |

Masked diffusion inherits DDPM's **iterative multi-step generation** and **progressive corruption schedule** while operating in MLM's **discrete token space** with **masking as corruption**.

## Key Methods

### D3PM — Discrete Denoising Diffusion Probabilistic Models
**Authors**: Austin et al. (2021)
**Key idea**: Generalizes the DDPM framework from continuous to discrete state spaces using discrete transition matrices. The absorbing-state variant (where tokens can only transition to `[MASK]`) is the purest form of masked diffusion. Demonstrates that variational lower bounds from DDPM transfer directly to discrete spaces.

### Multinomial Diffusion
**Authors**: Hoogeboom et al. (2021)
**Key idea**: Defines diffusion over categorical distributions using multinomial transition kernels. Each token's category distribution diffuses toward a uniform distribution over the vocabulary, rather than toward an absorbing mask state.

### MaskGIT — Masked Generative Image Transformer
**Authors**: Chang et al. (2022)
**Key idea**: Applies masked prediction to image generation using a bidirectional Transformer (not U-Net). During training, randomly masks a fraction of visual tokens and predicts them. During inference, starts from fully masked tokens and iteratively unmasks in order of model confidence. Achieves competitive image generation quality with ~8-16 decoding steps (vs. DDPM's 1000).

### MDLM — Masked Diffusion Language Models
**Authors**: Sahoo et al. (2024)
**Key idea**: Simplifies discrete diffusion for text by using absorbing-state masking with a continuous-time formulation. Achieves competitive perplexity with autoregressive models on text benchmarks while enabling parallel decoding and infilling.

## Significance

1. **Theoretical unification**: Proves that BERT-style masking and DDPM-style diffusion are special cases of the same framework — a discrete vs. continuous instantiation of the corrupt-then-reconstruct paradigm
2. **Faster generation**: MaskGIT generates images in 8-16 steps vs. DDPM's 1000, by leveraging parallel prediction at each unmasking step
3. **Discrete data generation**: Enables diffusion-quality generation for inherently discrete data (text, categorical features, codebook tokens) without the continuous relaxation tricks needed to apply Gaussian diffusion to discrete spaces
4. **Bidirectional generation**: Unlike autoregressive models (left-to-right), masked diffusion generates all positions in parallel with iterative refinement — enabling infilling, editing, and non-causal generation

## Potential Applications

- **Tabular data synthesis**: Generating synthetic categorical features for fraud detection training data (extending the TabSyn approach referenced in [Diffusion Model](term_diffusion_model.md) from continuous to mixed categorical-continuous data)
- **Text generation with controllability**: Iterative unmasking allows editing and infilling — useful for generating adversarial abuse text for model robustness testing
- **Fast image generation**: MaskGIT's 8-step generation could enable real-time adversarial CAPTCHA generation (vs. Stable Diffusion's slower pipeline)

## Related Terms

- [Diffusion Model](term_diffusion_model.md) — Continuous-space parent framework; masked diffusion is its discrete counterpart
- [Masked Language Model](term_mlm.md) — Single-step discrete masking for representation learning; masked diffusion extends this to multi-step generation
- [Self-Supervised Learning](term_ssl.md) — Both MLM and diffusion are SSL methods; masked diffusion sits at their intersection
- [Transformer](term_transformer.md) — Architecture used by MaskGIT, MDLM, and most modern masked diffusion models
- [BERT](term_bert.md) — Pioneered discrete masking as a training objective; masked diffusion extends BERT's paradigm to generation
- [Computer Vision](term_computer_vision.md) — MaskGIT applies masked diffusion to image generation
- [Anomaly Detection](term_anomaly_detection.md) — Reconstruction error from masked diffusion could serve as a discrete anomaly score

## References

- Austin et al., "Structured Denoising Diffusion Models in Discrete State-Spaces" (D3PM), NeurIPS 2021
- Hoogeboom et al., "Argmax Flows and Multinomial Diffusion", NeurIPS 2021
- Chang et al., "MaskGIT: Masked Generative Image Transformer", CVPR 2022
- Sahoo et al., "Simple and Effective Masked Diffusion Language Models" (MDLM), NeurIPS 2024
- [Thought: Corrupt-Then-Reconstruct — BERT vs. DDPM](../analysis_thoughts/thought_corrupt_then_reconstruct_bert_ddpm.md) — Comparative analysis that motivated this term note
- [DDPM — Ho et al., 2020](../papers/lit_ho2020denoising.md) — Foundational continuous diffusion paper
- [BERT — Devlin et al., 2019](../papers/lit_devlin2019bert.md) — Foundational discrete masking paper
