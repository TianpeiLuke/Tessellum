---
tags:
  - resource
  - terminology
  - reinforcement_learning
  - policy_optimization
  - efficient_inference
  - reasoning
keywords:
  - CISPO
  - clipped importance-sampled policy optimization
  - off-policy RL
  - reasoning RL
  - importance sampling
  - clipped objective
  - MiniMax-M1
  - reasoning chain compression
topics:
  - Reinforcement Learning for LLMs
  - Policy Optimization
  - Efficient Inference
language: markdown
date of note: 2026-04-18
status: active
building_block: concept
related_wiki: null
---

# CISPO (Clipped Importance-Sampled Policy Optimization)

## Definition

**CISPO (Clipped Importance-Sampled Policy Optimization)** is a reinforcement learning algorithm for fine-tuning large language models that clips importance sampling weights rather than per-token probability ratios. Originally introduced by MiniMax in their MiniMax-M1 technical report (MiniMax et al., 2025), CISPO was designed to improve training stability for long-chain reasoning tasks where standard PPO-style clipping degrades performance.

The key insight is that PPO clips the ratio of new-to-old policy probabilities at the *token level*, which can suppress rare but critical tokens (mathematical operators, domain-specific symbols). CISPO instead clips the *importance sampling weight* (the product of per-token ratios across the full sequence), preserving the contribution of individual rare tokens while still bounding the overall update magnitude. This produces smoother policy updates and better sample efficiency for long reasoning sequences.

## Context

CISPO sits within the family of policy optimization algorithms for LLM post-training, positioned between on-policy methods (PPO, GRPO) and fully off-policy methods (DPO, offline RL). It addresses a specific failure mode of PPO in reasoning tasks: when generating long chains of thought (thousands of tokens), PPO's per-token clipping accumulates conservatively, effectively freezing the policy on sequences where even a few tokens have high probability ratios.

In the MEMENTO framework (Kontonis et al., 2026), CISPO is applied after two-stage supervised fine-tuning to improve memento quality. The RL signal is binary correctness of the final answer — if the model reaches the right answer despite compressing its reasoning chain, the policy is reinforced. CISPO's off-policy capability is critical here because MEMENTO uses the vLLM block masking extension for rollouts, where the inference environment differs from the training environment.

## Key Characteristics

- **Clips importance weights, not token ratios**: Unlike PPO which clips `π_new(a|s) / π_old(a|s)` per token, CISPO clips the product `∏_t π_new(a_t|s_t) / π_old(a_t|s_t)` at the sequence level — bounding the overall update while preserving per-token gradients
- **Off-policy capable**: Can reuse rollouts from a different policy version, reducing the computational cost of generating new samples for each update step
- **KL penalty regularization**: Uses a KL divergence penalty (β = 0.001 in MEMENTO) to prevent excessive drift from the SFT reference policy
- **Block cap constraint**: In MEMENTO, a 7K-token block cap prevents degenerate compression behaviors where the model generates extremely long blocks to avoid summarization
- **Better sample efficiency**: Fewer rollouts needed per update compared to on-policy methods like PPO or GRPO, since off-policy data can be reused
- **Smoother training dynamics**: The sequence-level clipping produces less noisy gradient estimates than per-token clipping, especially for long sequences
- **Outcome-based reward**: In MEMENTO, uses binary correctness (right/wrong final answer) rather than process-based or human preference rewards
- **Recovers 1.2-1.8pp accuracy**: In MEMENTO experiments, CISPO post-training recovers accuracy lost during SFT across model scales (8B to 32B)

## Comparison with Related RL Algorithms

| Algorithm | Clipping Target | On/Off-Policy | Reward Type | Sequence Length Sensitivity |
|-----------|----------------|---------------|-------------|---------------------------|
| **PPO** | Per-token probability ratio | On-policy | Any (process or outcome) | High — accumulates conservative clipping |
| **CISPO** | Sequence-level importance weight | Off-policy | Any (outcome in MEMENTO) | Low — single clip per sequence |
| **GRPO** | Group-level relative ranking | On-policy | Outcome (group comparison) | Medium — normalizes within groups |
| **DPO** | N/A (implicit reward) | Offline | Preference pairs | Low — no rollouts needed |
| **DAPO** | Dynamic per-token clipping | On-policy | Outcome | Medium — adapts clip range |
| **REINFORCE** | None (raw gradient) | On-policy | Any | Very high — high variance |

## Limitations

- **Limited public documentation**: CISPO was introduced in a technical report (MiniMax-M1) without a standalone paper — the algorithm details are less thoroughly analyzed than PPO or DPO
- **Sequence-level approximation**: Clipping at the sequence level may be too coarse for very long sequences where different segments require different update magnitudes
- **Hyperparameter sensitivity**: The interaction between the clipping threshold, KL penalty (β), and block cap requires careful tuning — no systematic ablation has been published
- **Binary reward limitation**: In MEMENTO, the binary correctness signal cannot distinguish between "almost right" and "completely wrong" compressions
- **Requires SFT initialization**: CISPO is applied after SFT — it cannot be used for training from scratch

## Related Terms

- **[PPO](term_ppo.md)**: CISPO's direct predecessor — both clip to bound updates, but PPO clips per-token ratios while CISPO clips sequence-level importance weights
- **[GRPO](term_grpo.md)**: Alternative group-based policy optimization; GRPO ranks within groups while CISPO uses importance sampling across the full batch
- **[DPO](term_dpo.md)**: Offline alternative that avoids rollouts entirely by learning from preference pairs; CISPO requires online rollouts but gains from outcome-based rewards
- **[Reinforcement Learning](term_rl.md)**: CISPO is an RL algorithm in the policy gradient family, specialized for language model optimization
- **[RLHF](term_rlhf.md)**: Broader paradigm; CISPO uses outcome-based rewards rather than human preference rewards, but could be combined with learned reward models
- **[RLAIF](term_rlaif.md)**: Related paradigm using AI-generated feedback; CISPO's binary correctness signal is simpler than RLAIF's model-generated preferences
- **[Reward Model](term_reward_model.md)**: CISPO in MEMENTO bypasses learned reward models by using binary correctness — a design choice that avoids reward hacking
- **[Policy Gradient](term_policy_gradient.md)**: CISPO is a policy gradient method with importance sampling correction for off-policy data
- **[Fine-Tuning](term_fine_tuning.md)**: CISPO is applied as a post-SFT fine-tuning stage — it refines a model already trained with supervised learning
- **[Block Masking](term_block_masking.md)**: The vLLM block masking extension enables CISPO training rollouts in MEMENTO by physically evicting KV cache entries during generation
- **[KV Cache](term_kv_cache.md)**: CISPO's training objective in MEMENTO implicitly optimizes for KV cache efficiency — better mementos lead to more KV cache reduction
- **[Chain of Thought](term_chain_of_thought.md)**: CISPO optimizes the quality of compressed chain-of-thought reasoning — the reasoning chain is the content being compressed by mementos

## References

- [MiniMax et al. (2025). "MiniMax-01: Scaling Foundation Models with Lightning Attention." Technical Report](https://arxiv.org/abs/2501.08313) — introduces CISPO
- [Kontonis et al. (2026). "MEMENTO: Teaching LLMs to Manage Their Own Context." arXiv:2604.09852](https://arxiv.org/abs/2604.09852) — applies CISPO for post-SFT reasoning improvement
- [MEMENTO (Kontonis et al., 2026)](../papers/lit_kontonis2026memento.md) — vault literature note
