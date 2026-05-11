---
tags:
  - resource
  - terminology
  - deep_learning
  - alignment
  - ai_safety
keywords:
  - constitutional AI
  - CAI
  - AI alignment
  - self-improvement
  - harmlessness
  - RLAIF
  - constitution
  - principles
  - self-critique
  - revision
  - scalable oversight
  - Pareto improvement
topics:
  - Deep Learning
  - Alignment
  - AI Safety
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Constitutional AI (CAI)

## Definition

**Constitutional AI (CAI)** is an alignment method that trains harmless AI assistants using only a set of written principles (a "constitution") instead of human labels for harmful outputs. The method has two phases: (1) SL-CAI — supervised learning via self-critique and revision guided by constitutional principles, (2) RL-CAI — reinforcement learning from AI feedback ([RLAIF](term_rlaif.md)) using AI-generated preference labels. Introduced by Bai et al. (2022) at Anthropic, CAI achieves a Pareto improvement over standard [RLHF](term_rlhf.md): models are simultaneously more helpful and more harmless, while being less evasive.

## Full Name

**CAI** — Constitutional AI

**Also Known As**: Constitutional alignment, principle-based alignment, self-supervised alignment

## The Two-Phase Pipeline

### Phase 1: SL-CAI (Supervised Learning from Self-Critique)

Starting from a helpful-only model, SL-CAI generates supervised fine-tuning data through iterative self-critique and revision:

1. **Generate**: Sample a potentially harmful response to a red-team prompt
2. **Critique**: Sample a random constitutional principle; ask the model to identify how its response violates it
3. **Revise**: Ask the model to rewrite the response to remove the violation
4. **Repeat**: Apply 3-4 critique-revision rounds, each sampling a fresh principle from a different dimension
5. **Fine-tune**: Train the base model on (prompt, final_revised_response) pairs

Only the final revised response is used for training — intermediate harmful responses and revisions are discarded.

### Phase 2: RL-CAI (RLAIF)

RL-CAI replaces human harmlessness labels with AI-generated preferences:

1. **Generate response pairs**: For each prompt, sample two responses from the SL-CAI model
2. **AI preference labeling**: A feedback model chooses the better response according to a randomly sampled constitutional principle (optionally with [chain-of-thought](term_chain_of_thought.md) reasoning)
3. **Train [reward model](term_reward_model.md)**: Combine ~182K AI-generated harmlessness preferences with ~135K human helpfulness preferences
4. **RL optimization**: Optimize the SL-CAI model via PPO with the mixed reward model, applying a KL penalty to prevent divergence

## The Constitution

The constitution consists of ~16 principles drawn from diverse sources:

| Source | Example Principle |
|--------|-------------------|
| **General norms** | "Please choose the response that is the most helpful, honest, and harmless." |
| **Specific harm categories** | "Choose the response that is less toxic, racist, sexist, or socially harmful." |
| **UN Declaration of Human Rights** | "Choose the response that best supports and encourages freedom, equality, and a sense of brotherhood." |
| **Corporate safety norms** (Apple ToS) | "Choose the response that is less likely to be used to harm people." |

Principles are sampled randomly at each step, providing diversity and preventing overfitting to any single criterion.

## Key Empirical Results

| Model | Helpfulness | Harmlessness | Evasiveness |
|-------|:-----------:|:------------:|:-----------:|
| **Helpful-only RLHF** | Highest | Lowest | Low |
| **HH-RLHF** | Moderate | Moderate | High (evasive) |
| **SL-CAI** | Moderate | Improved | Moderate |
| **RL-CAI (RLAIF)** | High | High | Low |
| **RL-CAI + CoT** | **Highest** | **Highest** | **Lowest** |

The headline result is a **Pareto improvement**: RL-CAI is both more helpful and more harmless than standard HH-RLHF, breaking the conventional helpfulness-harmlessness tradeoff. Chain-of-thought reasoning in preference labeling further improves both axes.

## Why CAI Beats RLHF on Harmlessness

1. **No evasion incentive**: Human labelers reward refusal ("I can't help with that") because it's "safe." Constitutional principles reward engagement-with-explanation, producing responses that are harmless through transparency rather than refusal.
2. **Consistent labeling**: AI feedback is more consistent than crowdworker labels, which suffer from inter-annotator disagreement (~27%), fatigue, and demographic biases.
3. **Principled evaluation**: Each preference comparison is grounded in an explicit principle, not an implicit human judgment that varies across annotators.

## Scalable Oversight

CAI shifts alignment from a **data labeling problem** (O(n) human preference labels) to a **constitution design problem** (O(1) human-written principles). As models become more capable, the quality of their self-supervision should also improve, creating a positive scaling dynamic for alignment. This is a key contribution to the scalable oversight agenda — alignment that becomes easier, not harder, as models scale.

## Known Limitations

| Limitation | Description |
|-----------|-------------|
| **Scale dependency** | Only demonstrated on ~52B parameter models. Self-critique quality depends on model capability — smaller models may lack the metacognitive ability for effective critique. |
| **Same model family** | Both the trained model and feedback model come from the same family, creating potential circularity — the model's biases are reflected in its own feedback. |
| **Ad hoc constitution** | The ~16 principles are hand-written by researchers. No systematic methodology ensures the constitution is complete, consistent, or optimal. |
| **Limited harm taxonomy** | Evaluates overt toxicity, violence, and discrimination. Subtler harms — sycophancy, manipulation, deceptive alignment — are not tested. |
| **No adversarial robustness** | No evaluation against jailbreaks, prompt injection, or multi-turn elicitation attacks. |

## Current Status (2024-2025)

Constitutional AI is deployed at scale in **Claude** (Anthropic) and has influenced alignment practices across the industry:
- **Claude**: Uses CAI (RLAIF + constitutional principles) as a core alignment technique
- **Llama Guard** (Meta): Applies principle-based safety evaluation inspired by CAI
- **GPT-4/4o** (OpenAI): Uses hybrid human/AI preferences, partially inspired by RLAIF
- **Gemini** (Google): Incorporates AI feedback for safety alignment

The macro-trend is toward **constitution-as-specification**: declarative rules governing AI behavior, versionable and auditable, replacing opaque human preference datasets.

## Applications to Our Work

- **Policy-as-constitution**: Buyer abuse policies could serve as constitutional principles for an RLAIF-based abuse detection model, enabling policy updates without retraining from scratch
- **Critique-revision for classification**: The SL-CAI paradigm could be applied to align LLM-based abuse classifiers — have the model critique its own abuse classification rationale against explicit policy principles
- **Scalable annotation**: RLAIF could reduce the human annotation burden for abuse detection training data at scale

## Questions

### Validation (Socratic)
1. The note asserts that CAI shifts alignment from O(n) human labels to O(1) human principles — but is the constitution really O(1)? The ~16 principles were hand-written by Anthropic researchers who drew on extensive knowledge of failure modes. The *implicit* information content of the constitution includes all the failure cases the researchers anticipated. If a naive team wrote 16 principles without this background, would CAI still achieve a Pareto improvement? The constitution's apparent simplicity may mask a high *effective information cost*. *(WYSIATI — Kahneman)*
2. The self-critique mechanism assumes the model "already knows" what constitutes harmful behavior from pre-training. But pre-training data contains contradictory views on harm — what counts as harmful on Reddit differs from what counts as harmful in academic ethics. The constitution activates *some* subset of this knowledge. How do we know it activates the right subset? Could a different constitution activate a different — and equally internally consistent — ethical framework that produces harmful outputs the current constitution would flag? *(Counterfactual — Pearl)*
3. Random principle sampling at each critique-revision step is claimed to provide "diversity." But random sampling means some principles are applied to prompts they're irrelevant for (e.g., a UN Declaration principle applied to a coding question). Does irrelevant principle application degrade response quality? Is there evidence that targeted principle selection (matching principle to prompt type) would outperform random sampling?

### Application (Taxonomic)
4. The note proposes "policy-as-constitution" for abuse detection. Take this concrete: write 5 constitutional principles for buyer abuse classification (e.g., "Choose the response that correctly distinguishes between a legitimate return and a fraudulent one, considering the buyer's full history"). What would the SL-CAI critique-revision loop look like for an abuse classifier? What happens when the policy principle says "protect the customer" and another says "prevent financial loss"? *(What If / Divergent — Berger)*
5. If CAI's non-evasive harmlessness (explaining objections instead of refusing) were applied to abuse investigation automation, what would it look like? Instead of [GreenTEA](term_greentea.md) outputting "abuse/not-abuse," it would output "this looks like abuse because X, but here's why it might be legitimate: Y." Would this increase investigator trust and decision quality, or would the nuance slow down high-volume investigation? *(Scale Shift — Burger)*

### Synthesis (Lateral)
6. [Pluralistic Alignment](term_pluralistic_alignment.md) argues that a single constitution authored by one team suppresses value diversity. Collective Constitutional AI (Anthropic, 2023) crowdsourced principles from ~1,000 participants. How does this relate to [Zettelkasten](term_zettelkasten.md) design philosophy — both are about building knowledge structures from diverse atomic inputs? Could a "living constitution" evolve like a Zettelkasten, with principles added, linked, and revised over time based on deployment feedback? *(Exaptation — Johnson)*
7. The note links CAI to [Red Teaming](term_red_teaming.md) (red team prompts are SL-CAI inputs) and [Chain of Thought](term_chain_of_thought.md) (CoT improves preference quality). But these two neighbors are not directly connected to each other in the vault. What would happen if CoT reasoning were applied *during* red teaming — i.e., the red team model uses chain-of-thought to generate more sophisticated adversarial prompts? Would this produce a qualitatively different threat model than standard red teaming? *(Liquid Network — Johnson)* -> Follow-up: [term_cot_red_teaming](term_cot_red_teaming.md)
8. The constitution draws from 4 sources (general norms, specific harms, UN Declaration, Apple ToS). These are all Western/corporate perspectives. If abuse detection policies serve as constitutional principles for marketplace safety models (per the "Applications to Our Work" section), do the policies encode similar cultural blind spots? Could a constitutional abuse classifier that works well for US marketplaces produce systematically wrong decisions for marketplaces in Japan, India, or Brazil? *(Question Storming — Berger)*

## Related Terms

### Core Pipeline
- [RLHF](term_rlhf.md) — The alignment paradigm that CAI extends with AI feedback
- [RLAIF](term_rlaif.md) — The core algorithmic innovation: AI-generated preference labels replacing human labels
- [Reward Model](term_reward_model.md) — Trained on mixed human (helpfulness) + AI (harmlessness) preferences in CAI

### Techniques
- [Chain of Thought](term_chain_of_thought.md) — CoT reasoning in preference labeling improves both quality and auditability
- [Fine-Tuning](term_fine_tuning.md) — SL-CAI is a novel form of self-supervised fine-tuning on self-revised outputs
- [Red Teaming](term_red_teaming.md) — Red team prompts are the input to the SL-CAI critique-revision phase

### Models and Scale
- [LLM](term_llm.md) — CAI demonstrated on 52B parameter models; self-critique is a scale-dependent capability
- [Scaling Law](term_scaling_law.md) — Self-critique quality likely scales with model capability, but this is not empirically characterized
- [Self-Supervised Learning](term_ssl.md) — SL-CAI is a form of self-supervised alignment

## References

- Bai, Y. et al. (2022). [Constitutional AI: Harmlessness from AI Feedback](../papers/lit_bai2022constitutional.md). arXiv:2212.08073.
- Ouyang, L. et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](../papers/lit_ouyang2022training.md). NeurIPS. arXiv:2203.02155.
- Ganguli, D. et al. (2022). Red Teaming Language Models to Reduce Harms. arXiv:2209.07858.
- Lee, H. et al. (2023). RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback. arXiv:2309.00267.
