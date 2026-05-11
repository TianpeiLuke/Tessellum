---
tags:
  - resource
  - literature_note
  - deep_learning
  - alignment
  - ai_safety
  - reinforcement_learning
keywords:
  - Constitutional AI
  - CAI
  - RLAIF
  - reinforcement learning from AI feedback
  - harmlessness
  - self-improvement
  - self-critique
  - revision
  - constitution
  - preference model
  - red teaming
  - chain-of-thought
  - AI safety
  - alignment
topics:
  - Deep Learning
  - Alignment
  - AI Safety
  - Reinforcement Learning
domain: "AI Alignment"
language: markdown
date of note: 2026-03-08
paper_title: "Constitutional AI: Harmlessness from AI Feedback"
authors:
  - Yuntao Bai
  - Saurav Kadavath
  - Sandipan Kundu
  - Amanda Askell
  - Jackson Kernion
  - Andy Jones
  - Anna Chen
  - Anna Goldie
  - Azalia Mirhoseini
  - Cameron McKinnon
  - Carol Chen
  - Catherine Olsson
  - Chris Olah
  - Danny Hernandez
  - Dawn Drain
  - Deep Ganguli
  - Dustin Li
  - Eli Tran-Johnson
  - Ethan Perez
  - Jamie Kerr
  - Jared Mueller
  - Jeffrey Ladish
  - Joshua Landau
  - Kamal Ndousse
  - Kamilė Lukošiūtė
  - Liane Lovitt
  - Michael Sellitto
  - Nelson Elhage
  - Nicholas Schiefer
  - Noemí Mercado
  - Nova DaSarma
  - Robert Lasenby
  - Robin Larson
  - Sam Ringer
  - Scott Johnston
  - Shauna Kravec
  - Sheer El Showk
  - Stanislav Fort
  - Tamera Lanham
  - Timothy Telleen-Lawton
  - Tom Conerly
  - Tom Henighan
  - Tristan Hume
  - Sam Bowman
  - Zac Hatfield-Dodds
  - Benjamin Mann
  - Dario Amodei
  - Nicholas Joseph
  - Sam McCandlish
  - Tom Brown
  - Jared Kaplan
year: 2022
source: "arXiv:2212.08073"
venue: "arXiv preprint"
DOI: "10.48550/arXiv.2212.08073"
arXiv: "2212.08073"
semantic_scholar_id: "3936fd3c6187f606c6e4e2e20b196dbc41cc4654"
zotero_key: "8BIHUARV"
paper_notes:
  - paper_bai2022constitutional_intro.md
  - paper_bai2022constitutional_contrib.md
  - paper_bai2022constitutional_algo.md
  - paper_bai2022constitutional_exp_design.md
  - paper_bai2022constitutional_exp_result.md
status: active
building_block: hypothesis
---

# Constitutional AI: Harmlessness from AI Feedback

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Constitutional AI: Harmlessness from AI Feedback |
| **Authors** | Bai, Kadavath, Kundu, Askell, Kernion, ... Amodei, Kaplan et al. (51 authors) |
| **Year** | 2022 |
| **Venue** | arXiv preprint (Anthropic) |
| **DOI** | 10.48550/arXiv.2212.08073 |
| **arXiv** | [2212.08073](https://arxiv.org/abs/2212.08073) |
| **Citations** | 2,539 |

## Abstract

As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'. The process involves both a supervised learning and a reinforcement learning phase. In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences. We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF). As a result we are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them. Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making. These methods make it possible to control AI behavior more precisely and with far fewer human labels.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_bai2022constitutional_intro](paper_bai2022constitutional_intro.md) | RLHF limitations (human labelers teach evasion), motivation for scalable oversight, research gap |
| **Contribution** | [paper_bai2022constitutional_contrib](paper_bai2022constitutional_contrib.md) | 4 claimed contributions: SL-CAI, RL-CAI (RLAIF), Pareto improvement over RLHF, CoT transparency |
| **Algorithm** | [paper_bai2022constitutional_algo](paper_bai2022constitutional_algo.md) | Two-phase CAI pipeline: SL critique-revision + RL from AI feedback (RLAIF), constitution design |
| **Experiment Design** | [paper_bai2022constitutional_exp_design](paper_bai2022constitutional_exp_design.md) | 52B parameter models, 135K helpfulness + 182K harmlessness comparisons, Elo evaluation |
| **Experiment Result** | [paper_bai2022constitutional_exp_result](paper_bai2022constitutional_exp_result.md) | Pareto improvement on helpfulness-harmlessness frontier, RLAIF matches RLHF, CoT boosts quality |
| **Review** | [review_bai2022constitutional](review_bai2022constitutional.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY -->

**Introduction**: RLHF with human feedback creates a tension between helpfulness and harmlessness — models trained to be harmless become evasive and unhelpful. Human labelers inadvertently teach evasion rather than nuanced engagement with sensitive topics. Constitutional AI addresses this by replacing human harmlessness labels with AI self-supervision guided by written principles.

**Contribution**: The paper introduces Constitutional AI (CAI) with two phases: (1) SL-CAI uses self-critique and revision to generate harmless training data without human labels, (2) RL-CAI (RLAIF) trains a preference model from AI feedback rather than human feedback. The method achieves a Pareto improvement — simultaneously more helpful and more harmless than standard RLHF.

**Algorithm**: The SL phase samples red-team prompts, generates initial (harmful) responses, then iteratively critiques and revises them using randomly sampled constitutional principles. The RL phase generates response pairs, has an AI model choose the better response per a constitutional principle, and trains a preference model on ~182K AI-generated comparisons mixed with ~135K human helpfulness comparisons.

**Results**: Constitutional RL models are both more helpful and less harmful than RLHF models (Pareto improvement). Chain-of-thought reasoning in preference labeling further improves quality. The method scales AI oversight while requiring only ~10 human-written principles instead of thousands of human preference labels.

## Relevance to Our Work

- [RLHF](../term_dictionary/term_rlhf.md) — CAI directly extends RLHF by replacing human harmlessness feedback with AI feedback
- [Reward Model](../term_dictionary/term_reward_model.md) — CAI trains the reward model on AI-generated preferences (RLAIF) rather than human preferences
- [Chain of Thought](../term_dictionary/term_chain_of_thought.md) — CoT reasoning in preference labeling improves both quality and transparency of AI decisions
- [Fine-Tuning](../term_dictionary/term_fine_tuning.md) — SL-CAI phase is a specialized form of supervised fine-tuning on self-revised responses
- [InstructGPT (Ouyang et al., 2022)](lit_ouyang2022training.md) — Direct predecessor establishing the RLHF pipeline that CAI improves upon

## Questions

### Validation (Socratic)
1. The Pareto improvement (more helpful AND more harmless) is the headline claim — but is this a genuine causal effect of the constitutional framework, or could the same result be achieved by simply training on 2.3× more preference data (317K total vs. 135K)? What controlled experiment would distinguish data volume from data source as the causal factor? *(Causal vs. Correlational — Pearl, Ladder of Causation)*
2. What information is missing that would change the conclusion about RLAIF's viability? Specifically: the paper uses the same 52B model family for both training and evaluation. If a different model family produced the AI feedback, would the Pareto improvement hold — or is it an artifact of self-reinforcing biases within a single model family? *(WYSIATI — Kahneman)*
3. The constitutional principles are drawn from diverse sources (UN Declaration, Apple ToS, general norms), but what happens when principles contradict each other on a specific prompt? Is there evidence that the model handles principle conflicts consistently, or does random sampling mask systematic inconsistencies?

### Application (Taxonomic)
4. Can the critique-revision paradigm (SL-CAI) be adapted for abuse classification — e.g., having an LLM critique its own abuse detection rationale against explicit [buyer abuse policies](../term_dictionary/term_cap.md), then revise its classification? What would the "constitution" for abuse detection look like? *(Adjacent Possible — Johnson)*
5. How would Constitutional AI behave at 0.01× scale (a 500M parameter model) vs. 100× scale (a 5T parameter model)? The paper only tests at 52B — at what scale does self-critique become reliable enough for production safety, and at what scale might it develop failure modes not visible at 52B (e.g., deceptive alignment)? *(Scale Shift — Burger)*

### Synthesis (Lateral)
6. How does CAI's "non-evasive harmlessness" (explaining objections rather than refusing) relate to [Chain of Thought](../term_dictionary/term_chain_of_thought.md)'s interpretability? Both produce reasoning traces — but CoT traces are for task performance while CAI traces are for safety decisions. Could a unified framework produce both task reasoning AND safety reasoning in a single generation?
7. [GreenTEA](../term_dictionary/term_greentea.md) transforms SOPs into optimized LLM prompts for abuse detection. Could GreenTEA's evolutionary prompt optimization be combined with CAI's constitutional approach — evolving the constitution itself using automated feedback on abuse detection accuracy? *(Exaptation — Johnson)*
8. [InstructGPT](lit_ouyang2022training.md) and CAI both use the same 3-stage pipeline (SFT → RM → PPO), but InstructGPT relies entirely on human labels while CAI replaces harmlessness labels with AI. What would happen if we applied the same substitution to [Reward Model](../term_dictionary/term_reward_model.md) training for helpfulness — replacing human helpfulness labels with AI feedback too? Would a fully-RLAIF pipeline (no human labels at all) converge or collapse? *(Liquid Network — Johnson)* -> Follow-up: [[term_full_rlaif]]

## Related Documentation

### Paper Notes
- [paper_bai2022constitutional_intro](paper_bai2022constitutional_intro.md)
- [paper_bai2022constitutional_contrib](paper_bai2022constitutional_contrib.md)
- [paper_bai2022constitutional_algo](paper_bai2022constitutional_algo.md)
- [paper_bai2022constitutional_exp_design](paper_bai2022constitutional_exp_design.md)
- [paper_bai2022constitutional_exp_result](paper_bai2022constitutional_exp_result.md)

### Related Vault Notes
- [RLHF](../term_dictionary/term_rlhf.md)
- [Reward Model](../term_dictionary/term_reward_model.md)
- [Chain of Thought](../term_dictionary/term_chain_of_thought.md)
- [Fine-Tuning](../term_dictionary/term_fine_tuning.md)
- [LLM](../term_dictionary/term_llm.md)
- [Scaling Law](../term_dictionary/term_scaling_law.md)
- [Transformer](../term_dictionary/term_transformer.md)
- [Constitutional AI](../term_dictionary/term_constitutional_ai.md)
- [RLAIF](../term_dictionary/term_rlaif.md)
- [Red Teaming](../term_dictionary/term_red_teaming.md)

### Related Literature
- [InstructGPT (Ouyang et al., 2022)](lit_ouyang2022training.md) — Direct predecessor establishing the RLHF pipeline that CAI improves upon
- [Attention is All You Need (Vaswani et al., 2017)](lit_vaswani2017attention.md) — Foundational Transformer architecture underlying all models in this work
- [GPT-3 (Brown et al., 2020)](lit_brown2020language.md) — Large language model demonstrating in-context learning that CAI builds upon
