---
tags:
  - resource
  - terminology
  - machine_learning
  - adversarial_ml
  - security
  - robustness
keywords:
  - adversarial attack
  - adversarial example
  - adversarial perturbation
  - evasion attack
  - white-box attack
  - black-box attack
  - gradient-based attack
  - transfer attack
  - attack success rate
  - adversarial robustness
  - FGSM
  - PGD
  - GCG
  - INPAINTING
  - Pareto efficiency
topics:
  - Machine Learning
  - Adversarial ML
  - Security
  - Robustness
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Adversarial Attack

## Definition

An **adversarial attack** on a machine learning model is the construction of inputs that are deliberately crafted to cause the model to produce incorrect, harmful, or unintended outputs. In the LLM context, adversarial attacks construct prompts that induce targeted (often undesired) responses, exploiting the model's sensitivity to input perturbations. Adversarial attacks serve dual purposes: as **offensive tools** (finding model vulnerabilities for exploitation) and as **defensive tools** (stress-testing models for robustness via [red teaming](term_red_teaming.md) and adversarial training).

The phenomenon of adversarial vulnerability was first identified in computer vision (Szegedy et al. 2014), where imperceptible pixel perturbations could cause image classifiers to misclassify with high confidence. This discovery revealed a fundamental gap between human perception and learned decision boundaries. The concept has since been extended to all modalities — text, audio, tabular data — and has become a central concern in both ML security and AI safety.

## Full Name

**Adversarial Attack** (no standard acronym)

## Also Known As

- Adversarial example generation
- Evasion attack (when attacking a deployed classifier)
- Adversarial perturbation
- Input manipulation attack
- Model exploitation

## Attack Taxonomy by Access Level

The attacker's level of access to the target model fundamentally determines which attack strategies are available:

| Access Level | What the Attacker Has | Attack Strategies | Examples |
|:------------:|----------------------|-------------------|----------|
| **White-box** | Full model access: weights, gradients, activations, architecture | Gradient-based optimization, activation manipulation | GCG, PGD, FGSM, AutoDAN (gradient mode) |
| **Gray-box** | Partial access: logits, token probabilities, embeddings | Logit-based search, soft prompt optimization | Soft prompt attacks, embedding-space perturbations |
| **Black-box** | API-only: input text in, output text out (possibly with logprobs) | Query-based search, LLM-guided, generative sampling | PAIR, BoN, INPAINTING, role-playing jailbreaks |

**Practical significance**: Most real-world attacks on proprietary models (ChatGPT, Claude, Gemini) must be black-box, making black-box attack methods the most practically relevant threat.

## Attack Taxonomy by Optimization Strategy

Adversarial attacks also differ in how they search for effective adversarial inputs:

| Strategy | Mechanism | Pros | Cons | Examples |
|----------|-----------|------|------|----------|
| **Gradient-based** | Compute gradients of a loss function w.r.t. input tokens; optimize via backpropagation | Precise targeting; high ASR on source model | Requires gradient access; high-perplexity outputs; poor transferability | GCG (Zou et al. 2023), PGD (Madry et al. 2017), FGSM (Goodfellow et al. 2015) |
| **Search-based** | Evolutionary or genetic algorithms over the discrete token space | No gradient access needed | Slow convergence; limited exploration | Genetic attack (Alzantot et al. 2018), AutoDAN (genetic mode) |
| **LLM-guided** | Use an attacker LLM to iteratively generate and refine adversarial prompts using target model feedback | Natural language output; fully black-box | Expensive (many queries to both attacker and target LLMs) | PAIR (Chao et al. 2023), Tree of Attacks (Mehrotra et al. 2023) |
| **Sampling-based** | Random perturbations or variations; succeed by volume | Simple; cheap per sample; embarrassingly parallel | Low ASR on robust models; no systematic optimization | Best-of-N (BoN) sampling, random synonym substitution |
| **Generative / Amortized** | Sample adversarial inputs from a learned generative model (e.g., DLLM) | O(1) inference cost; low perplexity; transferable; efficient | Requires training the generative model; amortization gap | INPAINTING (Ludke et al. 2025) |

### The INPAINTING Paradigm Shift

Ludke et al. 2025 introduced a fundamentally new approach to adversarial prompt generation. Instead of **optimizing** an adversarial prompt for a specific target (GCG, PAIR), INPAINTING **samples** from a [Diffusion LLM](term_diffusion_llm.md) conditioned on the desired harmful response. This reframes adversarial attack as **conditional generation** rather than **optimization**, shifting from per-instance search (expensive) to [amortized inference](term_amortized_inference.md) (cheap per instance).

| Property | Optimization-based (GCG) | Amortized/Generative (INPAINTING) |
|----------|--------------------------|-----------------------------------|
| Cost per attack | O(thousands of gradient steps) | O(one diffusion forward pass) |
| Output quality | High-perplexity gibberish | Low-perplexity natural language |
| Transferability | Low (4% on ChatGPT-5) | High (53% on ChatGPT-5) |
| Defense evasion | Detected by perplexity filters | Evades perplexity filters |
| Model access needed | White-box (for gradient computation) | Black-box (only needs DLLM) |

## Historical Evolution

Adversarial attacks have evolved significantly from their origins in computer vision to modern LLM attacks:

### Computer Vision Era (2014-2020)

| Year | Method | Key Contribution | Reference |
|------|--------|------------------|-----------|
| 2014 | **L-BFGS attack** | First demonstration of adversarial examples: imperceptible perturbations fool classifiers | Szegedy et al. 2014 |
| 2015 | **FGSM** | Fast single-step attack using gradient sign; showed adversarial vulnerability is ubiquitous | Goodfellow et al. 2015 |
| 2017 | **PGD** | Multi-step iterative attack; defined the "strongest first-order adversary" used in adversarial training | Madry et al. 2017 |
| 2018 | **C&W attack** | Optimization-based attack that defeats defensive distillation | Carlini & Wagner 2017 |

### NLP Era (2018-2022)

| Year | Method | Key Contribution | Reference |
|------|--------|------------------|-----------|
| 2018 | **Genetic attack** | Evolutionary word substitution attack on text classifiers | Alzantot et al. 2018 |
| 2019 | **TextFooler** | Word-level perturbations preserving semantics | Jin et al. 2019 |
| 2020 | **Universal triggers** | Fixed token sequences that cause targeted model behavior across inputs | Wallace et al. 2019 |
| 2022 | **Prompt injection** | Adversarial instructions embedded in LLM inputs | Perez & Ribeiro 2022 |

### LLM Jailbreak Era (2023-Present)

| Year | Method | Key Contribution | Reference |
|------|--------|------------------|-----------|
| 2023 | **GCG** | First gradient-based jailbreak; universal adversarial suffixes | Zou et al. 2023 |
| 2023 | **PAIR** | LLM-guided black-box jailbreaking | Chao et al. 2023 |
| 2023 | **AutoDAN** | Readable jailbreaks via gradient + genetic search | Liu et al. 2023 |
| 2025 | **INPAINTING** | Paradigm shift: from optimization to inference via DLLMs | Ludke et al. 2025 |

The evolution from FGSM (2015) to INPAINTING (2025) represents a shift from **continuous perturbation** in a fixed norm ball to **discrete text generation** from a learned conditional distribution.

## Key Concepts

### Attack Success Rate (ASR)

The fraction of adversarial inputs that successfully cause the target model to produce the intended harmful/incorrect output. ASR is the primary metric for comparing attacks. In the jailbreak setting, ASR measures how often the model complies with a harmful request rather than refusing.

### Transferability

An adversarial example crafted against model A may also fool model B, even if B has different architecture and training. This is because models trained on similar data learn similar decision boundaries. Transferability enables [transfer attacks](term_transfer_attack.md) — the most practical threat to proprietary black-box models.

### Perplexity as a Defense Signal

Gradient-based attacks (GCG) produce high-perplexity adversarial suffixes — sequences of tokens that are statistically unlikely under a language model. Perplexity filtering detects these attacks by rejecting inputs with abnormally high perplexity. INPAINTING's key contribution is generating adversarial prompts with **low perplexity**, defeating this defense.

### Pareto Efficiency

Ludke et al. 2025 evaluate attacks along multiple dimensions simultaneously (ASR, perplexity, query cost) and show that INPAINTING Pareto-dominates other attacks — achieving higher ASR at lower perplexity with fewer queries. A Pareto-efficient attack is one where no other attack is simultaneously better on all metrics.

## Applications

### Offensive (Exploitation)

- **Jailbreaking**: Crafting prompts that bypass LLM safety alignment (see [Jailbreak](term_jailbreak.md))
- **Data extraction**: Adversarial prompts that cause models to leak training data
- **Misinformation**: Causing models to generate convincing false information
- **Capability elicitation**: Extracting capabilities (e.g., code for malware) that the model was trained to refuse

### Defensive (Robustness)

- **Adversarial training**: Including adversarial examples in training to harden models (PGD-based adversarial training)
- **Safety evaluation**: [Red teaming](term_red_teaming.md) uses adversarial attacks to discover vulnerabilities before deployment
- **Benchmark development**: Adversarial attack methods drive the creation of safety benchmarks (JailbreakBench, HarmBench)
- **Defense development**: Understanding attacks is necessary for developing effective defenses (perplexity filters, circuit breakers, LAT)

### Abuse Detection Relevance

- **Adversarial evasion**: Abusers may craft inputs to evade ML-based abuse detection classifiers
- **Model robustness testing**: Testing whether abuse detection models are robust to adversarial manipulation
- **Synthetic abuse generation**: Using adversarial methods to generate realistic abuse patterns for training data augmentation

## Related Terms

### Attack Types
- [Jailbreak](term_jailbreak.md) — Specific adversarial attack targeting LLM safety alignment
- [Transfer Attack](term_transfer_attack.md) — Adversarial attack that transfers across models
- [Red Teaming](term_red_teaming.md) — Broader practice that uses adversarial attacks for safety evaluation

### Generative Models for Attacks
- [Diffusion Model](term_diffusion_model.md) — Generative framework underlying the DLLM used in INPAINTING
- [Diffusion LLM](term_diffusion_llm.md) — Non-autoregressive LLM used as the adversarial generator in INPAINTING
- [Masked Diffusion](term_masked_diffusion.md) — Discrete diffusion variant used in LLaDA (the DLLM behind INPAINTING)
- [Amortized Inference](term_amortized_inference.md) — The paradigm that makes generative attacks efficient

### Alignment and Safety
- [RLHF](term_rlhf.md) — Alignment method that adversarial attacks test the robustness of
- [Reward Model](term_reward_model.md) — Component of RLHF that adversarial attacks may exploit
- [Constitutional AI](term_constitutional_ai.md) — Alignment method providing safety guardrails against adversarial prompts

## References

- Szegedy, C. et al. (2014). Intriguing Properties of Neural Networks. ICLR. arXiv:1312.6199. (First adversarial examples)
- Goodfellow, I. et al. (2015). Explaining and Harnessing Adversarial Examples. ICLR. arXiv:1412.6572. (FGSM)
- Madry, A. et al. (2017). Towards Deep Learning Models Resistant to Adversarial Attacks. ICLR 2018. arXiv:1706.06083. (PGD)
- Carlini, N. & Wagner, D. (2017). Towards Evaluating the Robustness of Neural Networks. IEEE S&P.
- Zou, A. et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043. (GCG)
- Chao, P. et al. (2023). Jailbreaking Black Box Large Language Models in Twenty Queries. arXiv:2310.08419. (PAIR)
- Liu, X. et al. (2023). AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models. arXiv:2310.04451.
- Ludke, D. et al. (2025). [Jailbreaking LLMs' Safeguard with Diffusion Language Models](../papers/lit_ludke2025diffusion.md). (INPAINTING — paradigm shift from optimization to inference)
