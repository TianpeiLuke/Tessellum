---
tags:
  - resource
  - literature_note
  - adversarial_attacks
  - ai_safety
  - diffusion_models
  - red_teaming
keywords:
  - diffusion LLM
  - DLLM
  - adversarial attack
  - jailbreaking
  - inpainting
  - amortized inference
  - transfer attack
  - prompt optimization
  - non-autoregressive
  - LLaDA
  - conditional generation
topics:
  - AI Safety
  - Adversarial Machine Learning
  - Diffusion Language Models
domain: "Generative Modeling"
language: markdown
date of note: 2026-03-08
paper_title: "Diffusion LLMs are Natural Adversaries for any LLM"
authors:
  - David Lüdke
  - Tom Wollschläger
  - Paul Ungermann
  - Stephan Günnemann
  - Leo Schwinn
year: 2025
source: "arXiv:2511.00203"
venue: "arXiv (preprint)"
DOI: "10.48550/arXiv.2511.00203"
arXiv: "2511.00203"
semantic_scholar_id: "5521922a591fb57aec78aba994250041cdf30282"
zotero_key: "HTTHF2NU"
paper_id: ludke2025diffusion
paper_notes:
  - paper_ludke2025diffusion_intro.md
  - paper_ludke2025diffusion_contrib.md
  - paper_ludke2025diffusion_algo.md
  - paper_ludke2025diffusion_exp_design.md
  - paper_ludke2025diffusion_exp_result.md
status: active
building_block: hypothesis
---

# Diffusion LLMs are Natural Adversaries for any LLM

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Diffusion LLMs are Natural Adversaries for any LLM |
| **Authors** | David Lüdke, Tom Wollschläger, Paul Ungermann, Stephan Günnemann, Leo Schwinn |
| **Year** | 2025 |
| **Venue** | arXiv (preprint) |
| **arXiv** | [2511.00203](https://arxiv.org/abs/2511.00203) |
| **Semantic Scholar** | [5521922a59...](https://www.semanticscholar.org/paper/5521922a591fb57aec78aba994250041cdf30282) |
| **Zotero** | HTTHF2NU |
| **Citations** | ~2 |

## Abstract

We introduce a novel framework that transforms the resource-intensive (adversarial) prompt optimization problem into an efficient, amortized inference task. Our core insight is that pretrained, non-autoregressive generative LLMs, such as Diffusion LLMs, which model the joint distribution over prompt-response pairs, can serve as powerful surrogates for prompt search. This approach enables the direct conditional generation of prompts, effectively replacing costly, per-instance discrete optimization with a small number of parallelizable samples. We provide a probabilistic analysis demonstrating that under mild fidelity assumptions, only a few conditional samples are required to recover high-reward (harmful) prompts. Empirically, we find that the generated prompts are low-perplexity, diverse jailbreaks that exhibit strong transferability to a wide range of black-box target models, including robustly trained and proprietary LLMs. Beyond adversarial prompting, our framework opens new directions for red teaming, automated prompt optimization, and leveraging emerging Flow- and Diffusion-based LLMs.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_ludke2025diffusion_intro](paper_ludke2025diffusion_intro.md) | LLMs sensitive to input perturbations; autoregressive models model q(y\|x) but adversarial prompting needs inverse q(x\|y); DLLMs model joint distribution enabling conditional sampling |
| **Contribution** | [paper_ludke2025diffusion_contrib](paper_ludke2025diffusion_contrib.md) | INPAINTING framework: amortized prompt search via DLLMs; probabilistic guarantees for sample-efficient discovery; efficient transferable black-box attacks |
| **Method** | [paper_ludke2025diffusion_algo](paper_ludke2025diffusion_algo.md) | Conditional sampling from pθ(x\|y*) via inpainting in pretrained DLLMs; surrogate/target fidelity assumptions; likelihood and reward guidance; vocabulary filtering |
| **Experiment Design** | [paper_ludke2025diffusion_exp_design](paper_ludke2025diffusion_exp_design.md) | 6 open-source target models + ChatGPT-5; LLaDA-8B as DLLM surrogate; JailbreakBench (100 behaviors); StrongREJECT judge; 5 baseline attacks (GCG, AutoDAN, PAIR, PGD, BoN) |
| **Experiment Results** | [paper_ludke2025diffusion_exp_result](paper_ludke2025diffusion_exp_result.md) | 100% ASR on most open-source models; 91-93% on robustly trained models; 53% on ChatGPT-5; Pareto-optimal efficiency; low perplexity comparable to benign prompts |
| **Review** | [review_ludke2025diffusion](review_ludke2025diffusion.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (4 review lenses applied) |

## Summary

- **Background**: Adversarial prompt optimization for LLMs is expensive and unreliable because autoregressive models parameterize q(y|x) but adversarial prompting requires solving the inverse problem q(x|y), forcing existing methods to rely on indirect search or heuristic optimization in discrete token space. Current automated attacks fall short of manual human red-teaming and produce high-perplexity prompts that are easily detected by filtering defenses. <!-- VERIFY: problem statement -->
- **Contribution**: The paper introduces INPAINTING, a framework that transforms costly per-instance adversarial prompt optimization into an amortized inference task by leveraging pretrained Diffusion LLMs (DLLMs), which model the joint distribution pθ(x, y) and enable direct conditional sampling of adversarial prompts pθ(x|y*) through inpainting-like conditioning. The authors provide probabilistic guarantees that under mild surrogate and target fidelity assumptions, only a small number of conditional samples suffices to recover high-reward prompts.
- **Method**: Given a target harmful response y*, the DLLM generates candidate prompts by running the reverse diffusion process while overwriting the response tokens with y* at each denoising step, yielding approximate samples from pθ(x|y*). Two optional guidance mechanisms -- likelihood guidance (biasing toward prompts with high target model likelihood P_f(y*|x)) and reward guidance (biasing toward high reward scores) -- can further improve attack success. Practical considerations include using the base (non-instruction-tuned) LLaDA-8B, stochastic masking of the conditioning target, and vocabulary filtering to remove special tokens. <!-- VERIFY: method details -->
- **Results**: INPAINTING achieves 100% attack success rate (ASR) on Phi-4-Mini, [Qwen](../term_dictionary/term_qwen.md)-2.5-7B, and Llama-3-8B; 91% on LAT Llama-3-8B and 93% on Circuit Breakers Llama-3-8B (robustly trained models); and 53% on ChatGPT-5 (vs. 13% for BoN, 4% for GCG). The method is Pareto-optimal in the ASR-vs-FLOPs tradeoff for most models and generates prompts with perplexity comparable to benign text, rendering perplexity-based defenses ineffective. <!-- VERIFY: exact numbers -->

## Relevance to Our Work

- **[Diffusion Model](../term_dictionary/term_diffusion_model.md)**: This paper applies diffusion model principles (iterative denoising, joint distribution modeling) to discrete text, demonstrating that DLLMs trained via masked diffusion can serve as powerful adversarial generators
- **[Masked Diffusion](../term_dictionary/term_masked_diffusion.md)**: The INPAINTING method relies on masked diffusion (LLaDA) where conditional generation is achieved by fixing response tokens during the denoising process
- **[Red Teaming](../term_dictionary/term_red_teaming.md)**: The paper presents a paradigm shift in automated red teaming -- from costly optimization-based attacks to efficient amortized inference via generative models
- **[Constitutional AI](../term_dictionary/term_constitutional_ai.md)**: Alignment defenses including constitutional AI are challenged by this attack, as low-perplexity adversarial prompts bypass filtering-based defenses
- **[RLHF](../term_dictionary/term_rlhf.md)**: RLHF-aligned models are shown to be vulnerable; the paper demonstrates successful attacks against robustly trained models (LAT, Circuit Breakers) and proprietary systems (ChatGPT-5)
- **[Reward Model](../term_dictionary/term_reward_model.md)**: The reward function Reward(y, x) plays a central role in both the theoretical framework (reward-weighted posterior) and practical evaluation (StrongREJECT judge)

## Related Documentation

### Paper Notes
- [Introduction](paper_ludke2025diffusion_intro.md)
- [Contribution](paper_ludke2025diffusion_contrib.md)
- [Method](paper_ludke2025diffusion_algo.md)
- [Experiment Design](paper_ludke2025diffusion_exp_design.md)
- [Experiment Results](paper_ludke2025diffusion_exp_result.md)

### Related Vault Notes
- [Diffusion Model](../term_dictionary/term_diffusion_model.md) — DDPM fundamentals; iterative denoising as generative process
- [Masked Diffusion](../term_dictionary/term_masked_diffusion.md) — Discrete diffusion via token masking (LLaDA architecture)
- [Red Teaming](../term_dictionary/term_red_teaming.md) — Adversarial safety evaluation of LLMs
- [CoT Red Teaming](../term_dictionary/term_cot_red_teaming.md) — Chain-of-thought attacks as complementary red-teaming strategy
- [Constitutional AI](../term_dictionary/term_constitutional_ai.md) — Alignment defense challenged by low-perplexity attacks
- [RLHF](../term_dictionary/term_rlhf.md) — Alignment context; RLHF-trained models as attack targets
- [Reward Model](../term_dictionary/term_reward_model.md) — Reward signal driving both attack optimization and evaluation

### Related Literature
- Ho et al. (2020). "Denoising Diffusion Probabilistic Models" — [lit_ho2020denoising](lit_ho2020denoising.md)
- Bai et al. (2022). "Constitutional AI: Harmlessness from AI Feedback" — [lit_bai2022constitutional](lit_bai2022constitutional.md)
- Touvron et al. (2023). "LLaMA: Open and Efficient Foundation Language Models" — [lit_touvron2023llama](lit_touvron2023llama.md)
- Zou et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models" — GCG baseline
- Chao et al. (2023). "Jailbreaking Black Box Large Language Models in Twenty Queries" — PAIR baseline
- Nie et al. (2025). "Large Language Diffusion Models" — LLaDA; the DLLM surrogate used in this work
