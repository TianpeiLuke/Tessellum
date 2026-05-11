---
tags:
  - resource
  - terminology
  - adversarial_ml
  - security
  - ai_safety
  - transferability
keywords:
  - transfer attack
  - adversarial transferability
  - surrogate model
  - black-box attack
  - cross-model attack
  - model-agnostic attack
  - decision boundary
  - shared vulnerability
  - INPAINTING transfer
  - GCG transfer
  - data-specific vulnerability
  - model-specific vulnerability
  - proprietary model attack
topics:
  - Adversarial ML
  - Security
  - AI Safety
  - Robustness
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Transfer Attack

## Definition

A **transfer attack** is an adversarial attack where adversarial examples crafted against one model (the **surrogate** or source model) are applied to a different model (the **target** or victim model) without any access to the target's internals. Transfer attacks exploit the observation that adversarial vulnerabilities are often shared across models trained on similar data or with similar architectures. In the LLM context, transfer attacks are particularly significant because they enable attacking proprietary black-box models (e.g., ChatGPT-5, Claude, Gemini) using only open-source surrogate models.

The existence of adversarial transferability was first observed by Szegedy et al. (2014) in computer vision and has been extensively studied since. In the LLM safety domain, transfer attacks represent the most realistic threat model: attackers do not have access to proprietary model weights but can use open-source models (Llama, LLaDA) as surrogates to craft attacks that transfer to closed-source targets.

## Full Name

**Transfer Attack** (also: Adversarial Transfer, Cross-Model Attack)

## Also Known As

- Adversarial transferability attack
- Surrogate-based attack
- Cross-model adversarial attack
- Model-agnostic adversarial attack
- Indirect adversarial attack

## Why Transfer Attacks Work

### Shared Decision Boundaries

Models trained on overlapping data distributions learn similar internal representations and decision boundaries. Even models with different architectures (Transformer vs. CNN, or different Transformer sizes) develop similar "vulnerable regions" in input space when trained on similar data.

| Factor | Effect on Transferability |
|--------|--------------------------|
| **Overlapping training data** | Higher transferability — models learn similar patterns |
| **Similar architecture** | Moderately increases transferability |
| **Similar training procedure** | Moderately increases transferability |
| **Similar model size** | Weak effect — transferability crosses scale boundaries |
| **Similar alignment method** | Increases jailbreak transferability (similar safety boundaries) |

### The INPAINTING Perspective: Data-Specific vs. Model-Specific Vulnerabilities

Ludke et al. 2025 offer a novel explanation for why INPAINTING achieves high transfer rates. They argue that INPAINTING's transferability is **data-specific** rather than **model-specific**:

**Traditional view (model-specific)**: Adversarial examples exploit specific model properties (gradient directions, decision boundary geometry). Transfer occurs when models happen to share similar properties.

**INPAINTING view (data-specific)**: The [Diffusion LLM](term_diffusion_llm.md) learns the joint distribution $p_\theta(x, y)$ of the shared training data. When it samples a prompt $x$ conditioned on a harmful response $y^*$, it generates text that would naturally co-occur with $y^*$ in the training data distribution. Any model trained on similar data — regardless of architecture, size, or alignment method — has learned these same natural co-occurrence patterns and is therefore vulnerable.

This explains a critical empirical finding: INPAINTING (which never sees the target model) achieves **53% ASR on ChatGPT-5**, while GCG (which is optimized directly against a white-box model) achieves only **4% ASR** when transferred. The optimization-based approach overfits to the surrogate model's specific decision boundary; the generation-based approach captures general data-level patterns.

### Formal Framework

Let $\mathcal{A}_S$ denote adversarial examples crafted against surrogate model $S$, and $\text{ASR}(A, T)$ denote the attack success rate of adversarial example set $A$ against target model $T$:

- **Source ASR**: $\text{ASR}(\mathcal{A}_S, S)$ — how well the attack works on the model it was crafted for
- **Transfer ASR**: $\text{ASR}(\mathcal{A}_S, T)$ — how well the attack works on the target model
- **Transfer rate**: $\frac{\text{ASR}(\mathcal{A}_S, T)}{\text{ASR}(\mathcal{A}_S, S)}$ — fraction of source-model successes that also succeed on target

High source ASR with low transfer rate indicates **overfitting to the surrogate** (characteristic of gradient-based attacks). High transfer rate (even with moderate source ASR) indicates **data-level vulnerability** (characteristic of generative attacks).

## Transfer Attack Categories

### Gradient-Based Transfer

| Property | Description |
|----------|-------------|
| **Surrogate** | Open-source LLM with accessible gradients (e.g., Llama, Vicuna) |
| **Method** | Optimize adversarial prompt/suffix using gradients from surrogate model |
| **Target** | Proprietary LLM (e.g., ChatGPT, Claude) |
| **Mechanism** | Optimized adversarial features happen to exploit shared decision boundary properties |
| **Limitation** | Tends to overfit to surrogate-specific gradient landscape |
| **Example** | GCG: optimize on Llama-2 → transfer to ChatGPT |

Techniques to improve gradient-based transfer:
- **Ensemble optimization**: Optimize against multiple surrogate models simultaneously
- **Input diversity**: Add random transformations during optimization to prevent surrogate overfitting
- **Momentum-based optimization**: Accumulate gradients across steps for smoother optimization landscape

### Generative Transfer (INPAINTING)

| Property | Description |
|----------|-------------|
| **Surrogate** | Diffusion LLM (LLaDA-8B) — not even the same type as the target |
| **Method** | Sample adversarial prompts from the DLLM's conditional distribution $p_\theta(x|y^*)$ |
| **Target** | Any LLM (autoregressive or not) |
| **Mechanism** | Generated prompts capture data-level co-occurrence patterns shared across models |
| **Advantage** | No per-instance optimization; low perplexity; high transfer rate |
| **Example** | INPAINTING: sample from LLaDA-8B → transfer to ChatGPT-5 |

### Prompt-Based Transfer

| Property | Description |
|----------|-------------|
| **Surrogate** | Attacker LLM (any model that can generate text) |
| **Method** | Use attacker LLM to craft natural-language jailbreak prompts |
| **Target** | Different LLM |
| **Mechanism** | Jailbreak patterns (role-playing, prompt injection) exploit common alignment weaknesses |
| **Example** | PAIR: GPT-4 as attacker → Llama-2 as target |

## Empirical Transfer Rates (Ludke et al. 2025)

The INPAINTING paper provides the most comprehensive comparison of transfer attack effectiveness on a frontier proprietary model:

### Transfer to ChatGPT-5

| Attack | Surrogate | ChatGPT-5 ASR | Perplexity | Transfer Type |
|--------|-----------|:--------------:|:----------:|:-------------:|
| **INPAINTING** | LLaDA-8B (DLLM) | **53%** | ~4.2 (low) | Generative |
| **BoN** | None (random sampling) | 13% | ~5.0 (low) | Sampling |
| **PAIR** | GPT-4 (attacker LLM) | ~10% | Low | Prompt-based |
| **GCG** | Llama-2 (gradient access) | 4% | ~1000+ (high) | Gradient-based |
| **PGD** | Llama-2 (gradient access) | 1% | ~500+ (high) | Gradient-based |
| **AutoDAN** | Llama-2 (gradient + genetic) | ~5% | ~50 (moderate) | Hybrid |

### Key Observations

1. **INPAINTING dominates**: 53% ASR — more than 4x the next best attack and 13x better than GCG
2. **Gradient-based attacks transfer poorly**: GCG (4%) and PGD (1%) — despite being the strongest on the surrogate model, they overfit to its specific decision boundary
3. **Perplexity correlates inversely with transfer**: Low-perplexity attacks (INPAINTING, BoN) transfer better than high-perplexity attacks (GCG, PGD)
4. **Architecture mismatch doesn't prevent transfer**: LLaDA-8B is a diffusion model (non-autoregressive) attacking an autoregressive model — fundamentally different architecture

### Transfer Across Multiple Targets

INPAINTING also demonstrates transfer across multiple target models:

| Target Model | INPAINTING ASR |
|-------------|:--------------:|
| Llama-3-8B (open-source) | High (source model family) |
| GPT-4 | Moderate-High |
| ChatGPT-5 | 53% |
| Claude (Anthropic) | Tested; results in paper |

The consistent transfer across diverse targets supports the data-specific vulnerability hypothesis.

## Implications for AI Safety

### 1. Proprietary Models Are Not Safe by Obscurity

The core security assumption of proprietary models is that attackers cannot access model weights. Transfer attacks violate this assumption:
- Any open-source model can serve as a surrogate
- DLLMs (even small ones) can generate highly transferable attacks
- As open-source models improve, surrogate quality will only increase

### 2. Small Models Threaten Large Models

INPAINTING demonstrates that an 8B-parameter DLLM can effectively attack models orders of magnitude larger and more expensive. This has profound implications:
- **Asymmetric threat**: The cost of attack is much lower than the cost of defense
- **Democratized attacks**: Open-source DLLMs are freely available; anyone can run them
- **Scale doesn't protect**: Target model size does not determine vulnerability to transfer attacks

### 3. Defense Implications

| Defense Strategy | Effectiveness Against Transfer Attacks |
|-----------------|---------------------------------------|
| **Perplexity filtering** | Effective against gradient-based transfer (high perplexity); ineffective against INPAINTING (low perplexity) |
| **Input paraphrasing** | May disrupt surface-level patterns but not semantic content |
| **Adversarial training** | Helpful if training includes transfer attack examples; expensive |
| **Semantic content analysis** | Most promising — analyzes meaning rather than surface statistics |
| **Latent space detection** | Promising — targets internal representations rather than input features |

### 4. The Arms Race Intensifies

The INPAINTING result suggests that transfer attacks will continue to improve as:
- Open-source DLLMs scale (from 8B to 70B+ parameters)
- Training data quality and quantity increase
- New conditional generation techniques emerge
- Multiple DLLMs can be ensembled for even higher transfer rates

## Historical Context

### Computer Vision Origins

Transfer attacks were first systematically studied in computer vision:

| Year | Finding | Reference |
|------|---------|-----------|
| 2014 | Adversarial examples transfer between different neural networks | Szegedy et al. 2014 |
| 2016 | Adversarial examples transfer across model families (CNN to SVM) | Papernot et al. 2016 |
| 2017 | Ensemble adversarial training improves robustness to transfer attacks | Tramer et al. 2017 |
| 2018 | Momentum-based attacks improve transferability | Dong et al. 2018 |

### Extension to NLP / LLMs

| Year | Finding | Reference |
|------|---------|-----------|
| 2023 | GCG suffixes show moderate transfer between aligned LLMs | Zou et al. 2023 |
| 2023 | PAIR jailbreaks show some cross-model transfer | Chao et al. 2023 |
| 2025 | INPAINTING achieves unprecedented transfer rates via generative approach | Ludke et al. 2025 |

The key evolution: from **perturbation-based transfer** (small changes to existing inputs) to **generation-based transfer** (creating entirely new inputs from a learned distribution).

## Relationship to Other Threat Models

| Threat Model | Access Required | Transfer Attack? | Example |
|-------------|----------------|:-----------------:|---------|
| **White-box** | Full model access | No (direct attack) | GCG on open-source model |
| **Black-box (query)** | API access with many queries | No (query-based) | PAIR |
| **Black-box (transfer)** | No access to target; use surrogate | **Yes** | INPAINTING: LLaDA → ChatGPT-5 |
| **Black-box (zero-query)** | No access to target; no queries | **Yes** (purest form) | Pre-computed transfer attacks |

Transfer attacks are the **most restrictive** yet **most realistic** threat model for attacking proprietary models. INPAINTING is notable because it is essentially a **zero-query transfer attack** — the adversarial prompts are generated entirely from the DLLM without ever querying the target model.

## Related Terms

### Attack Methods
- [Adversarial Attack](term_adversarial_attack.md) — Broad category; transfer attacks are a subcategory where surrogate and target models differ
- [Jailbreak](term_jailbreak.md) — Transfer attacks are a common strategy for jailbreaking proprietary models
- [Red Teaming](term_red_teaming.md) — Transfer attacks are a key technique in automated red teaming of black-box models

### Generative Models for Transfer
- [Diffusion LLM](term_diffusion_llm.md) — The DLLM (LLaDA) serves as the surrogate in INPAINTING's generative transfer attack
- [Masked Diffusion](term_masked_diffusion.md) — The discrete diffusion framework underlying LLaDA's conditional generation
- [Amortized Inference](term_amortized_inference.md) — Enables efficient transfer attack generation without per-instance optimization
- [Diffusion Model](term_diffusion_model.md) — Broader generative framework enabling the DLLM approach

### Safety and Alignment
- [Constitutional AI](term_constitutional_ai.md) — Alignment method whose safety boundaries transfer attacks attempt to circumvent
- [RLHF](term_rlhf.md) — Alignment training that may create shared vulnerable regions exploitable via transfer
- [Reward Model](term_reward_model.md) — Shared reward model properties may contribute to transferability

## References

- Szegedy, C. et al. (2014). Intriguing Properties of Neural Networks. ICLR. arXiv:1312.6199. (First observation of adversarial transferability)
- Papernot, N. et al. (2016). Transferability in Machine Learning: from Phenomena to Black-Box Attacks using Adversarial Samples. arXiv:1605.07277.
- Tramer, F. et al. (2017). Ensemble Adversarial Training: Attacks and Defenses. ICLR 2018. arXiv:1705.07204.
- Dong, Y. et al. (2018). Boosting Adversarial Attacks with Momentum. CVPR. arXiv:1710.06081.
- Zou, A. et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043. (GCG transfer)
- Chao, P. et al. (2023). Jailbreaking Black Box Large Language Models in Twenty Queries. arXiv:2310.08419. (PAIR)
- Ludke, D. et al. (2025). [Jailbreaking LLMs' Safeguard with Diffusion Language Models](../papers/lit_ludke2025diffusion.md). (INPAINTING — unprecedented transfer attack rates via generative approach)
