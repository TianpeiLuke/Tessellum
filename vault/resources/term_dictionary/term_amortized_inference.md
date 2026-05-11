---
tags:
  - resource
  - terminology
  - machine_learning
  - inference
  - optimization
  - probabilistic_modeling
keywords:
  - amortized inference
  - amortized optimization
  - inference network
  - variational autoencoder
  - VAE
  - recognition network
  - encoder network
  - per-instance optimization
  - forward pass inference
  - amortization gap
  - neural posterior estimation
  - conditional generation
  - INPAINTING
topics:
  - Machine Learning
  - Probabilistic Inference
  - Optimization
  - Generative Models
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Amortized Inference

## Definition

**Amortized inference** is the strategy of training a model to predict the solution to an inference problem directly, replacing per-instance optimization with a single forward pass through a learned function. Instead of solving a new optimization problem for each input (e.g., via MCMC, EM, or gradient descent), an amortized inference network learns to map inputs to approximate posterior distributions or optimal solutions in a single step, "amortizing" the cost of optimization across all instances seen during training.

The term "amortized" comes from the accounting concept: a large upfront cost (training the inference network) is spread across many future uses (each requiring only a cheap forward pass). This is analogous to compiling a program once to run it many times, versus interpreting it from scratch each time.

## Full Name

**Amortized Inference** (sometimes: Amortized Variational Inference, Amortized Optimization)

## Also Known As

- Amortized optimization
- Feed-forward inference
- Recognition network (in VAE literature)
- Inference network
- Encoder-based inference
- Neural approximate inference

## Core Idea

### Traditional vs. Amortized Inference

**Traditional inference** solves an optimization problem independently for each new input:

For each input $x$, find: $z^* = \arg\min_z \mathcal{L}(z; x)$

This requires running an iterative optimization algorithm (gradient descent, MCMC, EM) from scratch for every new $x$. The cost scales linearly with the number of instances.

**Amortized inference** trains a function $f_\theta$ that directly maps inputs to (approximate) solutions:

Train $f_\theta$ once such that: $f_\theta(x) \approx \arg\min_z \mathcal{L}(z; x)$ for all $x$

After training, inference for any new $x$ requires only a single forward pass through $f_\theta$. The per-instance cost drops from O(iterative optimization) to O(1 forward pass).

### Cost Structure

| Phase | Traditional Inference | Amortized Inference |
|-------|----------------------|---------------------|
| **Setup** | None | Train $f_\theta$ (expensive, one-time) |
| **Per instance** | Run optimizer from scratch (expensive) | Single forward pass (cheap) |
| **Total for N instances** | O(N * optimizer_cost) | O(training_cost + N * forward_pass) |
| **Break-even** | Always same cost | Amortized wins when N is large |

## Key Examples Across Domains

### Variational Autoencoders (Kingma & Welling, 2014)

The most canonical example of amortized inference:

| Component | Traditional VI | Amortized (VAE) |
|-----------|---------------|-----------------|
| **Goal** | Approximate posterior $q(z|x)$ | Approximate posterior $q_\phi(z|x)$ |
| **Method** | Optimize variational parameters per data point | Encoder network maps $x \to (\mu, \sigma)$ |
| **Cost per instance** | Many gradient steps | One forward pass through encoder |
| **Parameters** | Separate for each $x$ | Shared $\phi$ across all $x$ |

The VAE encoder $q_\phi(z|x)$ is the prototypical **recognition network** — a neural network trained to perform approximate posterior inference in a single forward pass. The key insight is that while the optimal $q(z|x)$ is different for each $x$, the **mapping** from $x$ to $q(z|x)$ can be learned as a single function.

### Adversarial Prompt Generation (Ludke et al. 2025)

INPAINTING applies amortized inference to adversarial attack generation:

| Component | Traditional (GCG) | Amortized (INPAINTING) |
|-----------|-------------------|------------------------|
| **Goal** | Find adversarial prompt $x$ that elicits harmful response $y^*$ | Sample adversarial prompt $x$ conditioned on $y^*$ |
| **Method** | Per-instance gradient descent on discrete tokens | [Diffusion LLM](term_diffusion_llm.md) conditional sampling $p_\theta(x|y^*)$ |
| **Cost per instance** | Thousands of gradient steps | One diffusion forward pass (~256 denoising steps) |
| **Output quality** | High-perplexity gibberish | Low-perplexity natural language |
| **Reusability** | Must restart for each new target | Same DLLM works for any target |

The [Diffusion LLM](term_diffusion_llm.md) (LLaDA-8B) serves as the amortized optimizer: it was trained once on text data and learned the joint distribution $p_\theta(x, y)$. To generate an adversarial prompt for any target response $y^*$, it simply samples from the conditional $p_\theta(x | y^*)$ via inpainting — no per-instance optimization needed.

### Bayesian Posterior Estimation (Cranmer et al. 2020)

In simulation-based inference, computing the posterior $p(\theta | x_\text{obs})$ traditionally requires MCMC for each new observation. Neural posterior estimation (NPE) trains a normalizing flow or mixture density network on simulated pairs $(\theta, x) \sim p(\theta)p(x|\theta)$ to directly predict $p(\theta | x)$ for any new observation.

### Combinatorial Optimization (Bengio et al. 2021)

Traditional combinatorial solvers (branch-and-bound, integer programming) solve each problem instance from scratch. Amortized approaches train graph neural networks on problem instances to predict solutions directly, achieving near-optimal results with orders-of-magnitude speedup at test time.

### Summary Table

| Domain | Traditional | Amortized | Reference |
|--------|-------------|-----------|-----------|
| Variational inference | Per-instance ELBO optimization | VAE encoder $q_\phi(z|x)$ | Kingma & Welling, 2014 |
| Adversarial prompting | Per-instance discrete search (GCG) | DLLM conditional sampling $p_\theta(x|y^*)$ | Ludke et al. 2025 |
| Bayesian posterior | MCMC per dataset | Neural posterior estimation | Cranmer et al. 2020 |
| Combinatorial optimization | Solver per instance | Graph neural network predictor | Bengio et al. 2021 |
| Image synthesis | Per-instance GAN inversion | Encoder-based GAN inversion | Richardson et al. 2021 |
| Hyperparameter tuning | Per-task Bayesian optimization | Meta-learned hyperparameter predictor | Hospedales et al. 2022 |

## In INPAINTING: The DLLM as Amortized Optimizer

The INPAINTING method (Ludke et al. 2025) makes the connection between amortized inference and adversarial attacks explicit:

### Why It Works

1. **Training (amortization phase)**: The DLLM (LLaDA-8B) is pretrained on massive text corpora, learning the joint distribution $p_\theta(x, y)$ over prompt-response pairs. This is the expensive one-time cost.

2. **Inference (amortized attack)**: To generate an adversarial prompt for a target harmful response $y^*$:
   - Fix $y^*$ as known tokens in the sequence
   - Mask the prompt positions
   - Run the diffusion reverse process to sample $x \sim p_\theta(x | y^*)$
   - The generated $x$ is an adversarial prompt that naturally pairs with $y^*$

3. **Cost**: Each new adversarial prompt requires only one diffusion forward pass (~256 denoising steps), regardless of the target response $y^*$.

### Why It's Better Than Per-Instance Optimization

| Advantage | Explanation |
|-----------|-------------|
| **Efficiency** | GCG requires ~100,000 gradient evaluations per prompt; INPAINTING requires ~256 denoising steps |
| **Quality** | Because the DLLM learned the natural text distribution, its samples have low perplexity (natural-sounding) |
| **Transferability** | The joint distribution is data-specific, not model-specific — patterns transfer across models trained on similar data |
| **Diversity** | Multiple diverse adversarial prompts can be sampled by running the diffusion process with different random seeds |
| **No gradient access** | INPAINTING does not need gradients through the target model — it's fully black-box |

## Advantages of Amortized Inference

1. **O(1) per-instance cost**: After the one-time training cost, each new inference is a single forward pass
2. **Parallelizable**: Multiple instances can be processed simultaneously in a batch
3. **Reusable**: The same trained network works for any new input without modification
4. **Smooth generalization**: The learned mapping can interpolate between seen examples, producing reasonable outputs for novel inputs
5. **End-to-end differentiable**: The inference network can be composed with downstream tasks and trained jointly

## Limitations

### The Amortization Gap

The amortized solution $f_\theta(x)$ is an **approximation** of the true per-instance optimum $z^* = \arg\min_z \mathcal{L}(z; x)$. The difference between the amortized and optimal solutions is called the **amortization gap**:

$$\text{Gap} = \mathcal{L}(f_\theta(x); x) - \mathcal{L}(z^*; x)$$

Sources of the amortization gap:
- **Limited network capacity**: $f_\theta$ may not be expressive enough to represent the optimal mapping
- **Training distribution mismatch**: If test inputs differ significantly from training data, the learned mapping may be inaccurate
- **Multi-modal posteriors**: If the true posterior is multi-modal, a single forward pass may only capture one mode

### Other Limitations

| Limitation | Description |
|------------|-------------|
| **Upfront training cost** | Training the inference network may be expensive; only worthwhile if many instances need to be processed |
| **Distribution coverage** | The network only works well for inputs similar to its training distribution |
| **Quality ceiling** | May never achieve the quality of per-instance optimization for individual instances |
| **Architecture constraints** | The inference network architecture constrains what solutions can be represented |

## Mathematical Formalization

### General Framework (Amos et al. 2023)

**Problem**: For a family of optimization problems parameterized by context $c$:
$$z^*(c) = \arg\min_{z \in \mathcal{Z}} f(z; c)$$

**Amortized approach**: Learn $\hat{z}_\theta(c) \approx z^*(c)$ by minimizing:
$$\min_\theta \mathbb{E}_{c \sim p(c)} \left[ \ell(\hat{z}_\theta(c), z^*(c)) \right]$$

or the direct objective:
$$\min_\theta \mathbb{E}_{c \sim p(c)} \left[ f(\hat{z}_\theta(c); c) \right]$$

### In VAEs

- Context $c = x$ (observed data)
- Solution $z$ (latent representation)
- Objective: ELBO = $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_\text{KL}(q_\phi(z|x) || p(z))$
- Inference network: $q_\phi(z|x)$ (encoder)

### In INPAINTING

- Context $c = y^*$ (target harmful response)
- Solution $x$ (adversarial prompt)
- Objective: $p_\theta(x | y^*)$ via diffusion inpainting
- Inference "network": The entire DLLM reverse process conditioned on $y^*$

## Related Terms

### Generative Models
- [Diffusion Model](term_diffusion_model.md) — Framework for the DLLM that serves as the amortized optimizer in INPAINTING
- [Diffusion LLM](term_diffusion_llm.md) — The specific model architecture (LLaDA) used as the amortized adversarial generator
- [Masked Diffusion](term_masked_diffusion.md) — The discrete diffusion variant that enables text-domain amortized generation

### Applications
- [Jailbreak](term_jailbreak.md) — INPAINTING uses amortized inference to generate jailbreak prompts
- [Adversarial Attack](term_adversarial_attack.md) — Amortized inference is the key innovation that makes INPAINTING efficient
- [Transfer Attack](term_transfer_attack.md) — Amortized inference enables transferable attacks because the learned distribution is data-specific

### Alignment
- [Reward Model](term_reward_model.md) — In INPAINTING, the reward model (StrongREJECT) evaluates the quality of amortized adversarial samples

- **[Conjugate Prior](term_conjugate_prior.md)**: Amortized inference replaces conjugate computation with learned neural approximation
- **[Dirichlet Distribution](term_dirichlet_distribution.md)**: Dirichlet-VAE uses amortized inference over Dirichlet posteriors
- **[Variational Inference](term_variational_inference.md)**: Amortized VI is the modern approach to approximate inference

## References

- Kingma, D. P. & Welling, M. (2014). Auto-Encoding Variational Bayes. ICLR. arXiv:1312.6114. (VAE — canonical amortized inference)
- Amos, B. (2023). Tutorial on Amortized Optimization. Foundations and Trends in Machine Learning. arXiv:2202.00665.
- Cranmer, K. et al. (2020). The Frontier of Simulation-Based Inference. PNAS. arXiv:1911.01429. (Neural posterior estimation)
- Bengio, Y. et al. (2021). Machine Learning for Combinatorial Optimization: A Methodological Tour d'Horizon. European Journal of Operational Research.
- Cremer, C. et al. (2018). Inference Suboptimality in Variational Autoencoders. ICML. arXiv:1801.03558. (Amortization gap analysis)
- Ludke, D. et al. (2025). [Jailbreaking LLMs' Safeguard with Diffusion Language Models](../papers/lit_ludke2025diffusion.md). (INPAINTING — amortized adversarial attack generation)
- Ho, J. et al. (2020). [Denoising Diffusion Probabilistic Models](../papers/lit_ho2020denoising.md). NeurIPS. arXiv:2006.11239.
