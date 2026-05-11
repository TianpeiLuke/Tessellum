---
tags:
  - resource
  - terminology
  - deep_learning
  - alignment
  - reinforcement_learning
keywords:
  - GRPO
  - group relative policy optimization
  - DeepSeek
  - verifiable rewards
  - RL alignment
  - mathematical reasoning
  - code generation
  - advantage estimation
  - critic-free RL
  - self-verification
topics:
  - Deep Learning
  - Alignment
  - Reinforcement Learning
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Group Relative Policy Optimization (GRPO)

## Definition

**Group Relative Policy Optimization (GRPO)** is a reinforcement learning alignment method that eliminates the need for a separate critic (value) model by estimating advantages at the group level. For each prompt, GRPO samples a group of responses, computes rewards for each (using verifiable signals like code execution or math verification), and normalizes rewards within the group to derive advantages. Introduced by DeepSeek (2025) in DeepSeek-R1, GRPO is particularly effective for domains with **verifiable rewards** — tasks where correctness can be automatically checked rather than requiring human judgment. GRPO demonstrates that RL can be applied directly to base models (without SFT), enabling large-scale reasoning capabilities to emerge through pure RL training.

## Full Name

**GRPO** — Group Relative Policy Optimization

**Also Known As**: Group-relative advantage estimation, critic-free RL alignment

## How GRPO Works

### Standard [PPO](term_ppo.md) (Comparison)

```
For each prompt:
  1. Generate response with policy π
  2. Score with reward model: r = RM(prompt, response)
  3. Estimate advantage using critic V: A = r - V(state)
  4. Update policy with clipped PPO objective
  5. Update critic V to improve advantage estimates
```

Requires: policy + reward model + critic (value function) = 3 models in memory.

### GRPO Algorithm

```
For each prompt x:
  1. Sample G responses: {y₁, y₂, ..., y_G} ~ π(· | x)
  2. Compute reward for each: rᵢ = R(x, yᵢ)    [verifiable reward]
  3. Normalize within group:
     Āᵢ = (rᵢ - mean(r₁..G)) / std(r₁..G)      [group-relative advantage]
  4. Update policy:
     L = -Σᵢ min(ρᵢ · Āᵢ, clip(ρᵢ, 1±ε) · Āᵢ) + β · KL(π ‖ π_ref)
     where ρᵢ = π(yᵢ|x) / π_old(yᵢ|x)
```

Requires: policy + reference model = 2 models in memory. No critic, no reward model.

### Key Innovation: Group-Relative Advantage

Instead of using a learned critic $V(s)$ to estimate advantages (which requires a separate model and introduces approximation error), GRPO uses the empirical statistics within a group of sampled responses:

$$\hat{A}_i = \frac{r_i - \mu_G}{\sigma_G}$$

This is simpler, requires no additional parameters, and is exact for the current sample.

## Verifiable Rewards

GRPO's distinguishing feature is its use of **verifiable rewards** — automated signals that don't require human judgment or a learned reward model:

| Domain | Verifiable Reward | Verification Method |
|--------|-------------------|---------------------|
| **Mathematics** | Answer correctness | Compare to ground truth; parse final answer |
| **Code generation** | Test pass rate | Execute code against test cases |
| **Formal proofs** | Proof validity | Check with proof assistant (Lean, Coq) |
| **Constraint satisfaction** | Rule compliance | Check format, length, content constraints |
| **Factual QA** | Answer accuracy | Compare to knowledge base |

### Why Verifiable Rewards Matter

- **No reward hacking**: The reward is ground truth, not a learned proxy — Goodhart's Law doesn't apply
- **No reward model needed**: Eliminates RM training, distribution shift, and overoptimization problems
- **Scales with compute**: More verification attempts cost compute, not human annotation
- **Binary signal, rich learning**: Even a simple correct/incorrect signal enables RL to discover sophisticated reasoning strategies

## DeepSeek-R1: GRPO at Scale

DeepSeek-R1 demonstrated GRPO's potential at scale:

| Finding | Detail |
|---------|--------|
| **RL without SFT** | Applied GRPO directly to the base model (no SFT stage), and reasoning emerged purely through RL |
| **Emergent behaviors** | The model spontaneously developed self-verification, reflection, and error-correction strategies |
| **"Aha moment"** | During training, the model learned to re-examine problems and change its approach — an emergent metacognitive behavior |
| **Math reasoning** | AIME 2024: 79.8% pass@1 (competitive with OpenAI o1) |
| **Chain-of-thought** | CoT reasoning emerged without being explicitly prompted — the model learned that thinking step-by-step improves verification pass rates |

## GRPO vs Other Alignment Methods

| Dimension | PPO (RLHF) | DPO | GRPO |
|-----------|:----------:|:---:|:----:|
| **Reward source** | Learned RM | Implicit (policy) | Verifiable (ground truth) |
| **Models in memory** | 4 (policy, RM, critic, ref) | 2 (policy, ref) | 2 (policy, ref) |
| **Advantage estimation** | Critic V(s) | N/A (offline) | Group normalization |
| **Online/offline** | Online | Offline | Online |
| **Reward hacking risk** | High | None (no explicit RM) | None (verifiable) |
| **Domain constraint** | General | General | Requires verifiable reward |
| **Exploration** | Yes (generates new responses) | No (fixed dataset) | Yes (group sampling) |

## Known Limitations

| Limitation | Description |
|-----------|-------------|
| **Requires verifiable rewards** | Only applicable where automated correctness checking is feasible. Creative writing, nuanced helpfulness, and ethical reasoning lack verifiable rewards. |
| **Group size tradeoff** | Larger groups (G) give better advantage estimates but cost proportionally more compute. Typical G = 8-64. |
| **Variance** | Group-level normalization can have high variance with small groups or when most responses are equally good/bad. |
| **Not general-purpose** | Cannot replace RLHF/DPO for general alignment (helpfulness, harmlessness) where no ground truth exists. |
| **Reward sparsity** | In hard domains, most sampled responses may be incorrect (r=0), providing limited learning signal. |

## Applications to Our Work

- **Abuse rule verification**: Abuse detection rules have verifiable outcomes — a rule either correctly classifies a transaction or doesn't. GRPO could optimize rule parameters using verification against labeled data without a learned reward model.
- **Investigation automation quality**: [GreenTEA](term_greentea.md) investigation decisions can be verified against ground truth outcomes (was the enforcement action upheld?). GRPO could optimize investigation prompts using these verifiable signals.
- **SQL/code generation**: Abuse analytics queries have verifiable outputs (query runs and returns expected results). GRPO could optimize LLM-generated SQL for abuse reporting.

## Related Terms

### Alignment Family
- [RLHF](term_rlhf.md) — The alignment paradigm GRPO simplifies by removing critic and RM
- [DPO](term_dpo.md) — Another RLHF simplification; offline and preference-based (vs. GRPO's online and reward-based)
- [Reward Model](term_reward_model.md) — GRPO eliminates the RM by using verifiable rewards
- [Constitutional AI](term_constitutional_ai.md) — CAI uses principled AI feedback; GRPO uses ground-truth verification

### Techniques
- [Chain of Thought](term_chain_of_thought.md) — CoT reasoning emerged spontaneously during GRPO training of DeepSeek-R1
- [Fine-Tuning](term_fine_tuning.md) — GRPO is an RL-based fine-tuning method
- [Scaling Law](term_scaling_law.md) — DeepSeek-R1 shows GRPO scaling properties for reasoning

### Models
- [LLM](term_llm.md) — GRPO applied to LLM alignment for reasoning tasks

- **[Concentration Inequality](term_concentration_inequality.md)**: GRPO advantage estimation uses concentration bounds for baseline subtraction
- **[CISPO](term_cispo.md)**: Clipped Importance-Sampled Policy Optimization — an alternative alignment method that, like GRPO, simplifies the RLHF pipeline but uses importance-sampled off-policy updates

## References

- DeepSeek-AI. (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948.
- Shao, Z. et al. (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models. arXiv:2402.03300.
- Rafailov, R. et al. (2023). Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS. arXiv:2305.18290.
- Ouyang, L. et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](../papers/lit_ouyang2022training.md). NeurIPS. arXiv:2203.02155.
