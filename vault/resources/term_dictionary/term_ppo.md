---
tags:
  - resource
  - terminology
  - reinforcement_learning
  - deep_rl
  - actor_critic
  - on_policy
  - llm_alignment
keywords:
  - PPO
  - Proximal Policy Optimization
  - clipped surrogate
  - policy gradient
  - RLHF
  - trust region
  - GAE
  - Schulman
topics:
  - Deep Reinforcement Learning
  - On-Policy Actor-Critic
  - LLM Alignment
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Proximal Policy Optimization (PPO)

## Definition

**Proximal Policy Optimization (PPO)** is an **on-policy [actor-critic](term_actor_critic.md)** reinforcement learning algorithm that uses a **clipped surrogate objective** to constrain policy updates, preventing destructively large steps. The key mechanism clips the probability ratio $r(\theta) = \pi_\theta(a \mid s) / \pi_{\theta_{old}}(a \mid s)$ to a range $[1-\varepsilon, 1+\varepsilon]$ (typically $\varepsilon = 0.2$):

$$J^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r(\theta) \hat{A}_t, \; \text{clip}(r(\theta), 1{-}\varepsilon, 1{+}\varepsilon) \hat{A}_t\right)\right]$$

where $\hat{A}_t$ is the estimated advantage, typically computed via **Generalized Advantage Estimation (GAE)**. The $\min$ operator forms a pessimistic lower bound — the policy cannot benefit from moving too far from $\pi_{old}$ in any single update, providing implicit trust-region behavior with only first-order optimization.

PPO is the **de facto standard algorithm for [RLHF](term_rlhf.md)** in LLM alignment and the most widely used on-policy deep RL algorithm.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| **2015** | Schulman et al. | **TRPO** — Trust Region Policy Optimization; KL-divergence constraint with second-order optimization; PPO's predecessor |
| **2016** | Schulman et al. | **GAE** — Generalized Advantage Estimation; TD($\lambda$)-style advantage estimator used by PPO |
| **2017** | Schulman, Wolski, Dhariwal, Radford & Klimov (OpenAI) | **PPO** — simplified TRPO using clipped surrogate; first-order only; matched or exceeded TRPO performance |
| **2019** | Berner et al. (OpenAI) | **OpenAI Five** — PPO scaled to defeat Dota 2 world champions using 256 GPUs |
| **2022** | Ouyang et al. (OpenAI) | **InstructGPT** — PPO as the RL step in RLHF; established PPO as the standard for LLM alignment |

## Two Variants

| Variant | Mechanism | Usage |
|---------|-----------|-------|
| **PPO-Clip** | Clips $r(\theta)$ to $[1-\varepsilon, 1+\varepsilon]$ | Default; simpler; better empirical performance |
| **PPO-Penalty** | Adaptive KL divergence penalty $\beta \, D_{KL}(\pi_{old} \| \pi_\theta)$; $\beta$ doubled if KL too large, halved if too small | Alternative; explicit KL control |

## Key Properties

- **On-policy**: Collects fresh experience per update batch, then discards it; multiple minibatch epochs per batch improve data utilization
- **Clipped surrogate**: First-order optimization with implicit trust region — simpler than TRPO's conjugate gradient; no second-order methods needed
- **Both discrete and continuous actions**: Unlike SAC (continuous only), PPO handles all action space types
- **Stable training**: Clipping prevents catastrophic policy degradation from large updates
- **GAE integration**: Advantage estimated via GAE($\lambda$), providing tunable bias-variance tradeoff analogous to [TD($\lambda$)](term_td_learning.md)
- **No monotonic improvement guarantee**: Unlike TRPO, PPO's clipping is heuristic — but empirically robust

## Applications

| Domain | System | Details |
|--------|--------|---------|
| **LLM Alignment** | InstructGPT, ChatGPT, Claude, GPT-4 | [RLHF](term_rlhf.md) pipeline — PPO optimizes LM policy against learned [reward model](term_reward_model.md) with KL penalty |
| **Game AI** | OpenAI Five (Dota 2) | Defeated world champions; 256 GPUs, 128K CPU cores, 180 years equivalent gameplay |
| **Robotics** | OpenAI Dactyl | Dexterous manipulation; same PPO code as OpenAI Five |
| **Standard benchmarks** | Atari, MuJoCo | Competitive with SAC on continuous control; strong on discrete (Atari) |

## Challenges and Limitations

1. **Sample inefficiency**: On-policy — cannot reuse past experience from replay buffers; requires many more interactions than off-policy methods (SAC, DQN)
2. **Hyperparameter sensitivity**: Clip parameter $\varepsilon$, learning rates, entropy coefficient, GAE $\lambda$, number of epochs all require tuning; reportedly "37 implementation details" matter
3. **No monotonic improvement**: Unlike TRPO's theoretical guarantees, PPO provides no formal assurance each update improves
4. **Scaling costs**: On-policy data collection at scale is expensive (OpenAI Five required massive compute)

## Related Terms

- **[Actor-Critic](term_actor_critic.md)**: Parent paradigm — PPO is the leading on-policy actor-critic variant
- **[SAC](term_sac.md)**: Off-policy actor-critic alternative; more sample-efficient but continuous actions only
- **[A2C](term_a2c.md)**: Simpler on-policy actor-critic without clipping; PPO's clipping provides more stable updates
- **[TD Learning](term_td_learning.md)**: PPO's critic uses TD learning; GAE is a TD($\lambda$)-style advantage estimator
- **[RLHF](term_rlhf.md)**: Uses PPO as the standard RL algorithm for LLM alignment
- **[Reward Model](term_reward_model.md)**: Provides the reward signal PPO optimizes against in RLHF
- **[Reinforcement Learning](term_rl.md)**: The parent paradigm — PPO is the most widely deployed deep RL algorithm
- **[CISPO](term_cispo.md)**: Clipped Importance-Sampled Policy Optimization — an alternative to PPO that uses importance sampling for off-policy updates while retaining clipped objectives

## References

### Vault Sources

### External Sources
- [Schulman, J. et al. (2017). "Proximal Policy Optimization Algorithms." arXiv](https://arxiv.org/abs/1707.06347) — PPO paper
- [Schulman, J. et al. (2015). "Trust Region Policy Optimization." ICML](https://arxiv.org/abs/1502.05477) — TRPO predecessor
- [Schulman, J. et al. (2016). "High-Dimensional Continuous Control Using Generalized Advantage Estimation." ICLR](https://arxiv.org/abs/1506.02438) — GAE paper
- [Ouyang, L. et al. (2022). "Training language models to follow instructions with human feedback." arXiv](https://arxiv.org/abs/2203.02155) — InstructGPT/RLHF
- [Huang, S. et al. (2022). "The 37 Implementation Details of Proximal Policy Optimization." ICLR Blog Track](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)
- [OpenAI Spinning Up: PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)
- [Wikipedia: Proximal policy optimization](https://en.wikipedia.org/wiki/Proximal_policy_optimization)
