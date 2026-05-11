---
tags:
  - resource
  - terminology
  - deep_learning
  - alignment
  - reinforcement_learning
keywords:
  - RLHF
  - reinforcement learning from human feedback
  - alignment
  - reward model
  - PPO
  - human preference
  - DPO
  - RLAIF
  - Constitutional AI
  - instruction following
  - KL penalty
  - PPO-ptx
topics:
  - deep_learning
  - alignment
  - reinforcement_learning
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Reinforcement Learning from Human Feedback (RLHF)

## Definition

**Reinforcement Learning from Human Feedback (RLHF)** is a post-training alignment technique that optimizes a language model's policy to maximize a learned reward signal derived from human preference comparisons. The canonical pipeline has three stages: (1) Supervised Fine-Tuning (SFT) on human demonstrations, (2) Reward Model (RM) training on pairwise preference comparisons, (3) Policy optimization via Proximal Policy Optimization (PPO) with a KL divergence penalty from the SFT model. RLHF established the standard recipe for aligning LLMs with human intent, adopted by ChatGPT, Claude, Gemini, and Llama-2.

## Full Name

**RLHF** — Reinforcement Learning from Human Feedback

**Also Known As**: Preference tuning, alignment training, human preference optimization

## The RLHF Pipeline

### Stage 1: Supervised Fine-Tuning (SFT)

Fine-tune a pre-trained LLM on high-quality (prompt, response) demonstrations written by human labelers. This produces a model that can follow instructions but may not reflect nuanced human preferences about what constitutes a "good" response.

- InstructGPT: ~13,000 demonstrations
- Typically 1–4 epochs with cosine LR decay

### Stage 2: Reward Model (RM) Training

Train a [Reward Model](term_reward_model.md) on human pairwise comparisons to predict which of two outputs a human would prefer. See the [Reward Model](term_reward_model.md) note for details on Bradley-Terry loss and architecture.

- InstructGPT: ~33,000 comparisons, 6B RM
- Output: scalar reward $r(\text{prompt}, \text{response})$

### Stage 3: Policy Optimization ([PPO](term_ppo.md))

Optimize the SFT policy using [PPO](term_ppo.md) to maximize the learned reward while staying close to the SFT model:

$$\text{objective}(\phi) = \mathbb{E}_{(x,y) \sim \pi_\phi} \left[ r_\theta(x, y) - \beta \cdot \text{KL}(\pi_\phi \| \pi_{\text{SFT}}) \right]$$

Where:
- $r_\theta(x, y)$ = reward model score for prompt $x$ and response $y$
- $\beta$ = KL penalty coefficient (prevents reward hacking)
- $\pi_\phi$ = the RL-optimized policy
- $\pi_{\text{SFT}}$ = the frozen SFT model (anchor)

**PPO-ptx variant** (Ouyang et al., 2022): Mixes pretraining gradients to prevent the "alignment tax" — regressions on general NLP capabilities:

$$\text{objective}(\phi) = \mathbb{E}\left[ r_\theta(x, y) - \beta \cdot \text{KL}(\pi_\phi \| \pi_{\text{SFT}}) \right] + \gamma \cdot \mathbb{E}_{x \sim \mathcal{D}_{\text{pretrain}}} \left[ \log \pi_\phi(x) \right]$$

## Historical Development

| Year | Paper | Contribution |
|------|-------|-------------|
| 2017 | Christiano et al. — Deep RL from Human Preferences | RLHF for robotics (Atari, MuJoCo). ~1 hour of human time for complex behaviors. Introduced pairwise comparison protocol. |
| 2019 | Ziegler et al. — Fine-Tuning LMs from Human Preferences | First RLHF for language models. ~5,000 comparisons for stylistic text generation, summarization, and question answering. |
| 2020 | Stiennon et al. — Learning to Summarize from Human Feedback | RLHF for summarization at scale. Established the SFT → RM → PPO pipeline. Showed RLHF summaries outperform larger supervised-only models. |
| 2022 | Ouyang et al. — [InstructGPT](../papers/lit_ouyang2022training.md) | **Production-scale RLHF for instruction-following.** 1.3B aligned model preferred over 175B unaligned GPT-3. Introduced PPO-ptx. Established RLHF as the industry standard. |
| 2022 | Bai et al. — Constitutional AI | **RLAIF**: Replace human labelers with AI-generated preferences guided by a "constitution" of ~10-16 principles. Two phases: SL-CAI (critique-revision) + RLAIF (AI preference training). |

## Variants and Alternatives

| Method | Paper | Key Idea | RM Required? |
|--------|-------|----------|-------------|
| **RLHF** | Ouyang et al., 2022 | Train RM → optimize with PPO | Yes |
| **RLAIF** | Bai et al., 2022 | AI generates preferences instead of humans | Yes (AI-trained) |
| **DPO** | Rafailov et al., 2023 | Reparameterize RLHF objective directly in terms of the policy; eliminate RM and PPO | No |
| **KTO** | Ethayarajh et al., 2024 | Kahneman-Tversky prospect theory; uses binary (good/bad) labels instead of pairs | No |
| **ORPO** | Hong et al., 2024 | Reference-free, single-stage monolithic preference training | No |
| **SimPO** | Meng et al., 2024 | Length-normalized average log-prob reward with target margin; no reference model | No |
| **GRPO** | DeepSeek, 2025 | Group Relative Policy Optimization; uses verifiable rewards (code, math) | Optional |

**DPO** is the most significant alternative — it shows that the RLHF objective can be solved in closed form without training a separate reward model, using only the policy itself. The DPO loss directly optimizes the policy on preference pairs:

$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}\left[ \log \sigma\!\left( \beta \cdot \left( \log \frac{\pi(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \log \frac{\pi(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right) \right) \right]$$

## Key Design Choices

### Why Pairwise Comparisons?

Relative judgments ("A is better than B") are more reliable and consistent than absolute ratings (Likert scales). Pairwise comparisons align with the Bradley-Terry model, providing a principled probabilistic foundation for learning preferences. Inter-annotator agreement is higher for comparisons (~73%) than for absolute scores.

### Why KL Penalty?

The KL divergence constraint $\beta \cdot \text{KL}(\pi_\phi \| \pi_{\text{SFT}})$ serves three functions:
1. **Anti-hacking**: Prevents the policy from exploiting reward model weaknesses (Goodhart's Law — "when a measure becomes a target, it ceases to be a good measure")
2. **Capability preservation**: Keeps the policy close to the SFT model, preserving general language abilities
3. **RM calibration**: The reward model was trained on outputs near the SFT distribution; predictions far from this distribution are unreliable

### Why PPO-ptx?

Standard PPO causes performance regressions on public NLP benchmarks (the "alignment tax"). PPO-ptx mixes pretraining gradients during RL, preventing catastrophic forgetting. In InstructGPT: RLHF total cost ~65 petaflops/s-days vs. 3,640 for GPT-3 pretraining — alignment is 56× cheaper than further scaling.

## Known Limitations

| Limitation | Description |
|-----------|-------------|
| **Reward hacking** | Policy learns to exploit reward model weaknesses rather than genuinely aligning (Goodhart's Law). Symptoms: verbose/sycophantic outputs that score high but aren't genuinely helpful. |
| **Mode collapse** | Policy converges to a narrow distribution of "safe" outputs, losing output diversity and creativity. |
| **Labeler bias** | Human preferences encode the biases of the labeler pool (~40 contractors in InstructGPT, primarily English-speaking, US/Southeast Asia). 27% inter-annotator disagreement reflects genuine value differences. |
| **Alignment tax** | RL optimization degrades performance on general NLP benchmarks (SQuAD, DROP). Mitigated by PPO-ptx but not eliminated. |
| **Training instability** | PPO requires careful hyperparameter tuning (β, learning rate, batch size). Large reward models (175B) were unstable in InstructGPT; only 6B was used. |
| **Instruction-dependent safety** | RLHF makes models follow instructions more faithfully — including harmful ones. Without safety guardrails, aligned models can be more dangerous than unaligned ones. |

## Current Status (2024-2025)

PPO-based RLHF remains foundational but is increasingly augmented:
- **Claude**: Constitutional AI (RLAIF) + RLHF
- **GPT-4/4o**: RLHF + AI feedback (hybrid human/AI preferences)
- **Llama-3**: SFT + rejection sampling + PPO + DPO (multi-round)
- **DeepSeek-R1**: GRPO with verifiable rewards (code execution, math verification)

The macro-trend is toward **RLAIF** (reducing reliance on human labelers) and **DPO-family methods** (eliminating RL complexity), but PPO-based RLHF remains the gold standard for the highest-stakes alignment applications.

## Applications to Our Work

- **Prompt-based abuse detection**: The RLHF-aligned LLMs (GPT-4, Claude) that power [AutoSignality](term_autosignality.md) and [GreenTEA](term_greentea.md) were trained with RLHF — understanding the pipeline explains their strengths (instruction following) and weaknesses (sycophancy, instruction-dependent safety)
- **Quality scoring for investigations**: A reward model trained on human abuse analyst preferences could score investigation quality, ranking analyst outputs by thoroughness and accuracy
- **Alignment tax awareness**: When fine-tuning LLMs for abuse detection, PPO-ptx's insight applies — mixing pretraining gradients prevents losing general language understanding

## Questions

### Validation (Socratic)
1. The note claims InstructGPT 1.3B aligned is "preferred over 175B unaligned GPT-3" — but preferred by whom? The 40 labelers were primarily English-speaking contractors from the US and Southeast Asia. Could this "alignment beats scale" result reverse for a different evaluator population (different cultural norms, different languages, different domains)? What would the causal DAG look like if labeler demographics were a confounding variable? *(Simpson's Paradox — Pearl)*
2. Imagine RLHF deployed at scale fails catastrophically — what assumption broke first? The pipeline assumes the reward model is a faithful proxy for human preferences, but the RM is trained on ~33K comparisons from ~40 labelers with 73% agreement. This means 27% of training signal is noise or genuine value disagreement being suppressed. Is the pipeline robust to systematic biases in this 27%, or could a coherent minority viewpoint (e.g., "honesty > politeness") be silently overwritten? *(Premortem — Kahneman)*
3. Is the definition of RLHF precise enough to distinguish it from [DPO](term_fine_tuning.md)? The note lists DPO as an "alternative" that eliminates the RM and PPO stages — but DPO still optimizes for human preferences using the same Bradley-Terry model. If the core of RLHF is "optimize policy for human preferences," then DPO *is* RLHF with a different optimizer. Where exactly is the boundary of this concept?

### Application (Taxonomic)
4. The note mentions [GreenTEA](term_greentea.md) and [AutoSignality](term_autosignality.md) as systems powered by RLHF-trained LLMs. Can we explain *why* RLHF specifically helps abuse detection — not just *that* it does? The mechanism would be: RLHF teaches instruction following → LLMs reliably follow abuse classification SOPs → consistent enforcement. But RLHF also teaches sycophancy and instruction-dependent safety → LLMs might agree with the analyst's hypothesis rather than challenge it. Which mechanism dominates in practice? *(Elaborative Depth — Brown)*
5. What new capability does RLHF unlock for buyer abuse prevention that was not feasible before? The note's "Applications to Our Work" section lists quality scoring, alignment tax awareness, and prompt-based detection. But the deeper adjacent possible may be: RLHF enables *preference-based model selection* — instead of optimizing abuse classifiers for precision/recall (which requires ground truth labels), optimize for *investigator preference* (which requires only pairwise comparisons). Could we train a [Reward Model](term_reward_model.md) on abuse analyst preferences to select between competing classifier outputs? *(Adjacent Possible — Johnson)*

### Synthesis (Lateral)
6. RLHF's core insight is that relative judgments ("A is better than B") are more reliable than absolute ratings. [Nexus](term_nexus.md) knowledge graph and [Abuse Polygraph](term_abuse_polygraph.md) both produce risk scores — absolute numbers. Could these systems be improved by switching to pairwise comparison frameworks? E.g., instead of "this buyer has abuse score 0.73," present pairs of buyer profiles and have analysts rank which is more suspicious — then train a reward model on these comparisons. *(Exaptation — Johnson)*
7. The note documents a clear trajectory: RLHF (2022) → RLAIF/[Constitutional AI](term_constitutional_ai.md) (2022) → DPO (2023) → GRPO (2025), with each step reducing reliance on human labels and RL complexity. [Scaling Law](term_scaling_law.md) shows capability scaling; this is an *alignment method scaling* trajectory. What is the extrapolated endpoint? If we project this trend forward, does alignment converge on fully automated self-improvement (no human feedback at all), or does it asymptote at a minimum irreducible human oversight? *(Liquid Network — Johnson)* -> Follow-up: [term_alignment_scaling_law](term_alignment_scaling_law.md)
8. The 27% inter-annotator disagreement in RLHF is treated as noise to be averaged over. But [Red Teaming](term_red_teaming.md) and [Constitutional AI](term_constitutional_ai.md) show that *what counts as harmful* is context-dependent and culturally variable. What if this 27% represents genuine value pluralism — different but equally valid perspectives on what "good" means? Could RLHF be extended to learn *multiple* reward models representing different value systems, rather than collapsing to a single majority preference? *(Question Storming — Berger)* -> Follow-up: [term_pluralistic_alignment](term_pluralistic_alignment.md)

## Related Terms

### Core Pipeline
- [Reward Model](term_reward_model.md) — Stage 2: learns human preferences as a scalar signal
- [Fine-Tuning](term_fine_tuning.md) — RLHF is a multi-stage fine-tuning pipeline (SFT → RM → PPO)

### Models and Architecture
- [LLM](term_llm.md) — RLHF is the standard post-training recipe for modern LLMs
- [Foundation Model](term_foundation_model.md) — RLHF demonstrates that foundation models need post-training alignment
- [Transformer](term_transformer.md) — Architecture underlying all RLHF-trained models

### Related Concepts
- [Transfer Learning](term_transfer_learning.md) — RLHF is a post-pretraining alignment transfer
- [Scaling Law](term_scaling_law.md) — InstructGPT's "1.3B beats 175B" challenges scale-first thinking
- [Self-Supervised Learning](term_ssl.md) — PPO-ptx preserves the SSL objective during RL
- **[CISPO](term_cispo.md)**: Clipped Importance-Sampled Policy Optimization — an alternative policy optimization algorithm used in RLHF-like training pipelines

### Formal Alternatives to Reward-Model Alignment
- **[Contestability](term_contestability.md)**: Formal property where a system's decisions can be challenged by modifying inputs/relations — an alternative to RLHF's implicit alignment via human preference data
- **[QBAF](term_qbaf.md)**: Quantitative Bipolar Argumentation Framework — substrate for replacing autoregressive RLHF outputs with structured argumentation that exposes its reasoning

## References

- Christiano, P. et al. (2017). Deep Reinforcement Learning from Human Preferences. NeurIPS. arXiv:1706.03741.
- Ziegler, D. et al. (2019). Fine-Tuning Language Models from Human Preferences. arXiv:1909.08593.
- Stiennon, N. et al. (2020). Learning to Summarize from Human Feedback. NeurIPS. arXiv:2009.01325.
- Ouyang, L. et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](../papers/lit_ouyang2022training.md). NeurIPS. arXiv:2203.02155.
- Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.
- Rafailov, R. et al. (2023). Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS. arXiv:2305.18290.
- Ethayarajh, K. et al. (2024). KTO: Model Alignment as Prospect Theoretic Optimization. ICML. arXiv:2402.01306.
- Brown, T. et al. (2020). [Language Models are Few-Shot Learners](../papers/lit_brown2020language.md). NeurIPS. arXiv:2005.14165.
