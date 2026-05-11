---
tags:
  - resource
  - terminology
  - cognitive_science
  - decision_making
  - communication
keywords:
  - computational kindness
  - cognitive burden
  - verification vs generation
  - decision reduction
  - choice architecture
topics:
  - decision making
  - cognitive science
  - communication
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Computational Kindness

## Definition

**Computational kindness** is the principle of reducing the computational (cognitive) burden on others by providing specific, constrained options rather than open-ended flexibility. The concept, from the conclusion of Christian & Griffiths' *Algorithms to Live By*, is grounded in a fundamental asymmetry in computational complexity: **verification is easier than generation**. Checking whether Tuesday at 2pm works (verification) is computationally trivial; generating all possible meeting times and selecting the best (generation) is computationally expensive. Therefore, proposing "Let's meet Tuesday at 2pm" is *kinder* than saying "I'm free whenever" — despite the latter feeling more accommodating.

## Full Name

**Computational Kindness** = Reducing Cognitive/Computational Burden

Also known as: **Cognitive Courtesy**, **Decision Reduction**

## How Computational Kindness Works

### Verification vs. Generation

| Operation | Complexity | Example |
|-----------|-----------|---------|
| **Generation** | Hard (often NP-hard) | "When are you free?" → must search all possible times, evaluate preferences, propose one |
| **Verification** | Easy (polynomial) | "Does Tuesday at 2pm work?" → check one calendar slot, yes/no |

The asymmetry is the same P ≠ NP principle that underpins modern cryptography: it's easy to verify a solution but hard to generate one.

### Specific vs. Open-Ended Communication

| Approach | What You Say | What You Impose |
|----------|-------------|----------------|
| **Open-ended** (seems kind) | "I'm flexible, whatever works for you" | Generation problem: recipient must search all options and propose |
| **Specific** (actually kind) | "How about Tuesday at 2pm, or Thursday at 10am?" | Verification problem: recipient checks 2 options, picks one |

## Practical Applications

1. **Meeting scheduling**: Propose 2–3 specific times rather than "when are you free?"
2. **Restaurant choice**: Suggest "How about Thai or Italian?" rather than "Where should we eat?"
3. **Decision-making in teams**: Present 2–3 concrete options with trade-offs rather than open-ended brainstorming
4. **Writing and communication**: Make specific recommendations with clear reasoning rather than presenting all possibilities
5. **Choice architecture**: Defaults and opt-out structures are computational kindness at scale

### Connection to Choice Architecture

[Choice architecture](term_choice_architecture.md) (Thaler & Sunstein) IS computational kindness applied at the system level. Setting defaults, structuring options, and reducing choice sets are all forms of reducing the computational burden on decision-makers.

### Connection to the Vault

The vault's design embodies computational kindness:
- **Term notes**: Provide specific definitions rather than requiring users to generate understanding from raw sources
- **Entry points**: Curate navigation paths rather than dumping all notes in a flat list
- **Digest notes**: Distill books into actionable frameworks rather than requiring full re-reads

## Related Terms

### Decision Science
- **[Term: Choice Architecture](term_choice_architecture.md)** — Nudge theory is computational kindness at the system level
- **[Term: Satisficing](term_satisficing.md)** — Constraining options for others enables their satisficing
- **[Term: Game Theory](term_game_theory.md)** — Computational kindness is cooperative game design; reducing others' decision costs

### Cognitive Science
- **[Term: Cognitive Bias](term_cognitive_bias.md)** — Choice overload (Schwartz's paradox of choice) is the failure mode computational kindness prevents
- **[Term: System 1 and System 2](term_system_1_and_system_2.md)** — Computational kindness routes decisions to System 1 (quick check) rather than System 2 (effortful generation)

### Source
- **[Digest: Algorithms to Live By](../digest/digest_algorithms_to_live_by_christian.md)** — Conclusion: Computational Kindness

## References

- Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Conclusion: Computational Kindness. Henry Holt and Company.
- Thaler, R.H. & Sunstein, C.R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press.
- Schwartz, B. (2004). *The Paradox of Choice: Why More Is Less*. Ecco.

---

**Last Updated**: March 12, 2026
**Status**: Active — Cognitive science, communication, and decision science
