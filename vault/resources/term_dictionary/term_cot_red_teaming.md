---
tags:
  - resource
  - terminology
  - ai_safety
  - evaluation
  - reasoning
keywords:
  - CoT red teaming
  - chain-of-thought red teaming
  - adversarial reasoning
  - reasoning-enhanced attacks
  - automated red teaming
  - jailbreak generation
  - adversarial prompt engineering
  - safety evaluation
topics:
  - AI Safety
  - Evaluation
  - Reasoning
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Chain-of-Thought Red Teaming (CoT Red Teaming)

## Definition

**Chain-of-Thought Red Teaming** is a concept combining [Chain of Thought](term_chain_of_thought.md) reasoning with [Red Teaming](term_red_teaming.md) to generate more sophisticated, strategically reasoned adversarial prompts. Standard automated red teaming generates attacks through simple sampling or gradient optimization; CoT red teaming has the attack model *reason step-by-step* about the target model's likely defenses, constitutional principles, and failure modes before crafting an adversarial prompt. This produces qualitatively different attacks — strategic rather than statistical — that more closely approximate expert human red teamers. The concept bridges two well-established vault notes (term_chain_of_thought and term_red_teaming) that are not directly linked but share complementary capabilities.

## Full Name

**CoT Red Teaming** — Chain-of-Thought Red Teaming

**Also Known As**: Reasoning-enhanced adversarial testing, strategic red teaming, deliberative attack generation, tree-of-attacks

## Standard Red Teaming vs. CoT Red Teaming

### Standard Automated Red Teaming

```
Input: Target model T, harm category H
For each attempt:
  prompt = RedTeamLM.generate("Write a prompt that makes T produce harmful output about H")
  response = T(prompt)
  success = is_harmful(response)
Output: Successful attack prompts
```

Attacks are generated without strategic reasoning — the red team model relies on its pre-training knowledge of attack patterns.

### CoT Red Teaming

```
Input: Target model T, harm category H, T's known defenses D (e.g., constitutional principles)
For each attempt:
  reasoning = RedTeamLM.chain_of_thought(
    "The target model uses [D] for safety. Step by step, analyze:
     1. What defense mechanisms would block a direct request about [H]?
     2. What assumptions do these defenses make?
     3. Where are the gaps between the letter and spirit of these defenses?
     4. Design an approach that exploits a specific gap."
  )
  prompt = RedTeamLM.generate_from_reasoning(reasoning)
  response = T(prompt)
  success = is_harmful(response)
Output: Attack prompts WITH reasoning traces explaining the attack strategy
```

The reasoning trace is as valuable as the attack itself — it documents the *theory of vulnerability* behind each successful attack.

## Why CoT Changes Red Teaming Quality

| Dimension | Standard Red Teaming | CoT Red Teaming |
|-----------|:--------------------:|:---------------:|
| **Attack sophistication** | Pattern-based (templates, paraphrases) | Strategy-based (exploit defense logic) |
| **Defense awareness** | None (black-box) | Explicit modeling of target defenses |
| **Multi-turn capability** | Limited (single-prompt focus) | Natural (reason about conversation dynamics) |
| **Attack diversity** | High volume, low variety | Lower volume, higher variety |
| **Auditability** | Only the attack prompt | Full reasoning trace explaining the strategy |
| **Defense improvement** | "Block this prompt" | "Fix this defense gap" |

### The Key Advantage: Reasoning Traces

When a CoT red team attack succeeds, the reasoning trace reveals *why* it succeeded:
- "The constitution says 'choose the less harmful response' but doesn't define harm for edge case X"
- "The safety training handles direct requests but not hypothetical framing"
- "Multi-turn escalation bypasses per-turn safety checks because context accumulates"

These traces are directly actionable for defense improvement — they transform red teaming from "find attacks" to "find defense gaps."

## Relationship to Existing Methods

### Tree of Attacks with Pruning (TAP) — Mehrotra et al., 2023

TAP is the closest existing method to CoT red teaming:
- Uses an LLM attacker that iteratively refines jailbreak prompts
- An LLM judge evaluates and prunes unpromising attack branches
- Tree search explores multiple attack strategies in parallel

TAP demonstrates that reasoning-enhanced attack generation produces more effective jailbreaks than simple prompting. CoT red teaming generalizes this to any harm category with explicit defense modeling.

### Crescendo — Microsoft, 2024

Multi-turn jailbreak approach that gradually escalates:
- Models the conversation as a persuasion process
- Each turn builds on previous context to normalize increasingly problematic requests
- CoT reasoning could enhance crescendo by planning the escalation strategy in advance

## Constitutional AI Interaction

CoT red teaming creates an interesting adversarial dynamic with [Constitutional AI](term_constitutional_ai.md):

1. **CAI defenses**: Constitutional principles define what the model should refuse
2. **CoT red teaming**: Reasons about gaps between principles and implementation
3. **Defense update**: Successful attacks reveal principle gaps → update constitution
4. **Arms race**: Updated constitution → new CoT attacks → further updates

This creates a productive **red team ↔ constitution co-evolution** cycle that progressively hardens the model's safety.

## Applications to Our Work

- **Abuse detection adversarial testing**: Sophisticated abusers don't use simple fraud patterns — they reason about detection rules and find gaps. CoT red teaming mirrors this adversarial reasoning process, testing abuse detection models against strategically crafted evasion attempts.
- **Policy gap discovery**: CoT red teaming against abuse policy-as-constitution would reveal gaps between policy intent and policy implementation — where the letter of the rule diverges from its spirit.
- **[GreenTEA](term_greentea.md) robustness**: Testing GreenTEA's SOP-following against strategically crafted edge cases that exploit gaps between SOP steps.
- **Investigator training**: CoT red team reasoning traces could serve as training material, showing investigators how sophisticated abusers think about detection evasion.

## Related Terms

### Core Components
- [Chain of Thought](term_chain_of_thought.md) — Provides the step-by-step reasoning capability applied to attack generation
- [Red Teaming](term_red_teaming.md) — The adversarial testing paradigm enhanced by CoT reasoning

### Alignment
- [Constitutional AI](term_constitutional_ai.md) — The defense system that CoT red teaming targets and helps improve
- [RLHF](term_rlhf.md) — Red team prompts feed into RLHF training; CoT-generated attacks may be more effective training data
- [RLAIF](term_rlaif.md) — AI-generated attacks with reasoning traces could improve AI preference labeling

### Related Concepts
- [Reward Model](term_reward_model.md) — CoT red teaming could target RM weaknesses specifically
- [LLM](term_llm.md) — Both the attacker (generating CoT attacks) and target are LLMs
- [Constitutional PRM](term_constitutional_prm.md) — Could evaluate defense reasoning step-by-step against attacks

## References

- Mehrotra, A. et al. (2023). Tree of Attacks: Jailbreaking Black-Box LLMs with Auto-Generated Subtrees. arXiv:2312.02119.
- Perez, E. et al. (2022). Red Teaming Language Models with Language Models. EMNLP. arXiv:2202.03286.
- Ganguli, D. et al. (2022). Red Teaming Language Models to Reduce Harms. arXiv:2209.07858.
- Bai, Y. et al. (2022). [Constitutional AI: Harmlessness from AI Feedback](../papers/lit_bai2022constitutional.md). arXiv:2212.08073.
- Zou, A. et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043.
- Russinovich, M. et al. (2024). Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack. arXiv:2404.01833.
