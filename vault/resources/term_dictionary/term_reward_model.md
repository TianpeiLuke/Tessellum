---
tags:
  - resource
  - terminology
  - deep_learning
  - alignment
  - reinforcement_learning
keywords:
  - reward model
  - RM
  - preference learning
  - Bradley-Terry
  - pairwise comparison
  - human feedback
  - reward hacking
  - overoptimization
  - process reward model
  - outcome reward model
  - PRM
  - ORM
topics:
  - deep_learning
  - alignment
  - reinforcement_learning
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Reward Model (RM)

## Definition

A **Reward Model (RM)** is a neural network trained on human pairwise preference comparisons to produce a scalar score $r(\text{prompt}, \text{response}) \to \mathbb{R}$ indicating how well a response aligns with human preferences. In the [RLHF](term_rlhf.md) pipeline, the reward model serves as a proxy for human judgment during policy optimization — the language model (policy) generates responses, the RM scores them, and PPO maximizes the RM score subject to a KL penalty. The RM is the critical bottleneck of the RLHF pipeline: it defines what "good" means.

## Full Name

**RM** — Reward Model

**Also Known As**: Preference model, value model (when used as [PPO](term_ppo.md) value function), critic (in [actor-critic](term_actor_critic.md) RL terminology)

## Training: Bradley-Terry Model

### Pairwise Comparison Framework

Human labelers compare $K$ model outputs for a given prompt and rank them. The RM learns to predict these preferences using the **Bradley-Terry model**, which models the probability that output $y_w$ is preferred over $y_l$:

$$P(y_w \succ y_l) = \sigma\!\left( r_\theta(x, y_w) - r_\theta(x, y_l) \right)$$

where $\sigma$ is the sigmoid function and $r_\theta$ is the scalar reward.

### Loss Function

$$\mathcal{L}(\theta) = -\frac{1}{\binom{K}{2}} \sum_{(y_w, y_l)} \log \sigma\!\left( r_\theta(x, y_w) - r_\theta(x, y_l) \right)$$

Summed over all $\binom{K}{2}$ pairwise comparisons from $K$ ranked outputs. InstructGPT uses $K = 4$ to $K = 9$ outputs per prompt, generating 6–36 comparison pairs per annotation.

### Key Training Detail (InstructGPT)

All $\binom{K}{2}$ pairs from a single prompt's $K$ outputs are processed as a single batch item, sharing the same forward pass. This prevents overfitting because the model cannot independently memorize each pair — it must learn a consistent reward function across all rankings for the prompt.

## Architecture

| Component | Description |
|-----------|-------------|
| **Base model** | Same architecture as the policy LLM (shared representation space) |
| **Initialization** | Initialized from the SFT model checkpoint |
| **Output head** | Final unembedding layer replaced by a linear projection to a single scalar |
| **Output position** | Scalar extracted from the last token's hidden state |
| **Normalization** | Bias term set so labeler demonstrations have mean reward = 0 |

### Size Selection

| Size Relative to Policy | Tradeoff |
|--------------------------|----------|
| **Same size** | Best representation alignment, highest cost |
| **Smaller** (InstructGPT: 6B RM for 175B policy) | Practical: cheaper, stable training. 175B RM was training-unstable |
| **Larger** | Rarely used; diminishing returns for preference prediction |

InstructGPT chose 6B because the 175B RM was prone to training divergence. The 6B RM achieves 72.4% accuracy on training labelers and 69.6% on held-out labelers — sufficient for PPO optimization.

## Key Challenges

### Reward Hacking (Goodhart's Law)

When the policy optimizes too aggressively against the RM, it finds "exploits" — outputs that score high on the RM but aren't genuinely preferred by humans. This is Goodhart's Law: "when a measure becomes a target, it ceases to be a good measure."

**Symptoms**: Verbose, sycophantic outputs; excessive hedging; formulaic structure that triggers high RM scores without substantive quality.

**Gao et al. (2023)** established scaling laws for reward model overoptimization: as PPO optimization pressure increases, the gold reward (actual human preference) follows a characteristic peak-then-decline curve. Key findings:
- RM size determines the overoptimization tolerance — larger RMs tolerate more optimization before gold reward declines
- Best-of-N sampling and PPO show different functional forms of overoptimization
- The optimal point is NOT maximum RM score, but a moderate optimization level

**Mitigation**: KL penalty (β coefficient), early stopping, reward model ensembles.

### Distribution Shift

The RM is trained on outputs from the SFT model. As PPO pushes the policy away from SFT, the RM must evaluate outputs increasingly far from its training distribution. RM predictions become unreliable in these out-of-distribution regions.

**Mitigation**: KL penalty constrains the policy to stay near SFT. Iterative RLHF (retrain RM on policy outputs) can partially address this but is expensive.

### Miscalibration and Sycophancy

If human labelers systematically prefer agreeable, confident-sounding outputs, the RM will learn to reward sycophancy. This propagates through PPO into the policy, producing models that tell users what they want to hear rather than what is true.

### Inter-Annotator Disagreement

With 72.6% agreement (InstructGPT), ~27% of cases reflect genuine value disagreement. The RM treats the majority preference as ground truth, systematically suppressing minority viewpoints. No standard methodology exists for handling value pluralism in reward modeling.

## Process vs. Outcome Reward Models

| Type | What It Scores | Training Data | Use Case |
|------|---------------|---------------|----------|
| **ORM** (Outcome RM) | Final answer correctness | Binary correct/incorrect labels | General alignment, QA |
| **PRM** (Process RM) | Each reasoning step | Step-level annotations (expensive) | Math, code, multi-step reasoning |

**Lightman et al. (2023)** introduced PRM800K — 800,000 step-level annotations for mathematical reasoning. PRMs enable:
- **Test-time scaling**: Use PRM to guide beam search or MCTS over reasoning steps
- **Error localization**: Identify exactly which step went wrong
- **Verification**: Score each step independently, catching errors early

**Tradeoff**: PRMs require step-level human annotation (10× more expensive than outcome labels). Recent work (2024) suggests discriminative ORMs are comparably robust to PRMs across diverse domains when scaled appropriately.

## Reward Model Scaling Laws

Gao et al. (2023, ICML) established power-law relationships for reward model overoptimization:

- **Larger RMs** tolerate more optimization before gold reward declines
- **Best-of-N**: Gold reward follows $R_{\text{gold}} = d \cdot \text{KL} - c \cdot \text{KL}^2$ (quadratic decline)
- **PPO**: Gold reward follows a similar but steeper decline curve
- **Implication**: RM size should scale with policy size and optimization budget — undersized RMs lead to faster overoptimization

**Practical recommendation**: Use RM ensembles (multiple RMs trained on different data splits) to improve robustness. The variance across ensemble members serves as an uncertainty estimate — high variance indicates unreliable reward predictions.

## Constitutional AI: Replacing Human RMs

Bai et al. (2022) introduced **Constitutional AI (CAI)**, which replaces human labelers with AI-generated preferences guided by a "constitution" of ~10-16 explicit principles:

1. **SL-CAI phase**: The model generates outputs, then critiques and revises them according to constitutional principles
2. **RLAIF phase**: AI generates preference labels (which output better satisfies the constitution?), trains an RM on these AI preferences, then runs PPO

**Advantages**: Consistent, scalable, transparent (principles are explicit). Eliminates labeler demographic bias.

**Limitations**: Circular reasoning risk (AI evaluating AI), self-reinforcing biases, bounded by the base model's capability to evaluate its own outputs.

## Applications to Our Work

- **Quality scoring for abuse investigations**: An RM trained on abuse analyst preferences could rank investigation outputs by thoroughness, evidence quality, and fairness
- **Understanding LLM behavior**: The reward models underlying GPT-4 and Claude shape how these models respond to abuse detection prompts — understanding RM limitations (sycophancy, overoptimization) explains potential failure modes
- **Preference-based model selection**: RM methodology could select between multiple abuse detection model outputs by learning investigator preferences

## Questions

### Validation (Socratic)
1. The Bradley-Terry model assumes preferences are **transitive** (if A > B and B > C, then A > C). But human preferences are frequently intransitive — especially in contested domains where different dimensions matter (response A is more helpful, B is more harmless, C is more concise). Under what fraction of real-world preference data does transitivity break down, and what happens to RM training when it does? Is the RM learning a consistent preference function or averaging over an inconsistent one? *(Causal vs. Correlational — Pearl)*
2. InstructGPT chose a 6B RM for a 175B policy because the 175B RM was "training-unstable." But this means the RM has 29× fewer parameters than the model it supervises — it's fundamentally less expressive. Imagine this choice failed completely: the 6B RM cannot represent the nuances of 175B-level outputs, and reward hacking succeeds because the policy finds exploits in the RM's compressed representation. What evidence would distinguish "6B is sufficient" from "6B is exploitable but the KL penalty masks the problem"? *(Premortem — Kahneman)*
3. The note states that [Pluralistic Alignment](term_pluralistic_alignment.md) challenges the single-RM assumption. But even within a single culture, the RM aggregates across annotators with 72.4% training accuracy. What does the remaining 27.6% error look like — is it random noise, or are there systematic patterns (e.g., the RM consistently misjudges safety-helpfulness tradeoffs)? Could this aggregate accuracy mask a Simpson's Paradox where the RM performs well on easy cases but fails on precisely the cases that matter most (controversial, safety-critical prompts)? *(Simpson's Paradox — Pearl)*

### Application (Taxonomic)
4. The note describes Process Reward Models (PRMs) that score each reasoning step individually. Could a PRM architecture be adapted for abuse investigation pipelines — scoring each step of an [ARI](term_ari.md) investigation (evidence gathering, pattern matching, decision justification) rather than just the final outcome? What would "step-level human annotation" look like for abuse investigation, and could it catch systematic errors that outcome-only evaluation misses? *(Adjacent Possible — Johnson)*
5. Can you explain *why* the KL penalty prevents reward hacking mechanistically, not just *that* it does? The note says it keeps the policy near the SFT distribution. But the SFT model was fine-tuned on demonstrations — its distribution already encodes certain biases. The KL penalty therefore constrains the policy to stay near a *biased* anchor. Is the KL penalty preserving safety or preserving bias? What experiment would distinguish these? *(Elaborative Depth — Brown)*

### Synthesis (Lateral)
6. The RM's core operation — producing a scalar score from a (prompt, response) pair — is structurally identical to what [Abuse Polygraph](term_abuse_polygraph.md) and [Nexus](term_nexus.md) do for buyer risk scoring. Both learn to map complex inputs to scalar risk/quality scores. Could the RM literature's insights on overoptimization, distribution shift, and Goodhart's Law directly inform how we detect and prevent "gaming" of abuse risk models? *(Exaptation — Johnson)*
7. The note documents an evolution: ORM → PRM → RM ensembles. Meanwhile, [RLAIF](term_rlaif.md) replaces the human labeler with an AI labeler, and [Constitutional AI](term_constitutional_ai.md) replaces the reward signal's source. If we combine these trends — PRM architecture + AI labelers + constitutional principles — we get a system where AI evaluates AI reasoning step-by-step against explicit principles. Is this converging toward automated alignment auditing? What would [GreenTEA](term_greentea.md)'s evolutionary prompt optimization look like if the fitness function were a step-level constitutional PRM? *(Liquid Network — Johnson)* -> Follow-up: [term_constitutional_prm](term_constitutional_prm.md)
8. The reward model defines what "good" means for the entire alignment pipeline. But what would an abuse detection [Reward Model](term_reward_model.md) specifically trained on investigator preferences optimize for? If we trained an RM on pairwise comparisons of investigation outputs (which investigation is "better"?), would it learn investigator skill or investigator bias? How would we distinguish these? *(Question Storming — Berger)* -> Follow-up: [[term_abuse_investigation_rm]]

## Related Terms

### RLHF Pipeline
- [RLHF](term_rlhf.md) — The reward model is Stage 2 of the RLHF pipeline
- [Fine-Tuning](term_fine_tuning.md) — RM is initialized from the SFT model, a fine-tuned checkpoint

### Models
- [LLM](term_llm.md) — Reward models share architecture with the LLMs they train
- [Foundation Model](term_foundation_model.md) — RMs are derived from foundation model checkpoints
- [Transformer](term_transformer.md) — RM architecture is Transformer + scalar head

### Related Concepts
- [Scaling Law](term_scaling_law.md) — Gao et al. (2023) scaling laws for RM overoptimization

## References

- Ouyang, L. et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](../papers/lit_ouyang2022training.md). NeurIPS. arXiv:2203.02155.
- Gao, L. et al. (2023). Scaling Laws for Reward Model Overoptimization. ICML. arXiv:2210.10760.
- Lightman, H. et al. (2023). Let's Verify Step by Step. ICLR 2024. arXiv:2305.20050.
- Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.
- Bradley, R.A. & Terry, M.E. (1952). Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons. Biometrika.
- Christiano, P. et al. (2017). Deep Reinforcement Learning from Human Preferences. NeurIPS. arXiv:1706.03741.
