---
tags:
  - resource
  - terminology
  - cognitive_science
  - decision_making
  - economics
  - game_theory
keywords:
  - game theory
  - Nash equilibrium
  - mechanism design
  - price of anarchy
  - Vickrey auction
  - incentive design
  - strategic interaction
topics:
  - decision making
  - cognitive science
  - economics
  - game theory
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Term: Game Theory

## Definition

**Game theory** is the mathematical study of strategic interaction — situations where the outcome for each participant depends on the actions of all participants. Christian & Griffiths focus on four key concepts: **Nash equilibrium** (a stable state where no player benefits from changing strategy unilaterally), **mechanism design** (designing rules so that selfish behavior produces good collective outcomes), **price of anarchy** (how much worse the selfish outcome is compared to the cooperative one), and **Vickrey auctions** (second-price sealed-bid auctions where truthful bidding is the dominant strategy). The central practical insight: **design systems where honest behavior is the best policy**, rather than relying on altruism.

## Full Name

**Game Theory** = Theory of Strategic Interaction

Also known as: **Strategic Decision Theory**, **Interactive Decision Theory**

## Core Concepts

| Concept | Definition | Human Application |
|---------|-----------|-------------------|
| **Nash Equilibrium** | State where no player benefits from unilateral change | The "status quo" everyone accepts even if no one likes it |
| **Price of Anarchy** | Ratio: (selfish outcome cost) / (optimal cooperative cost) | Measures the cost of decentralization and selfishness |
| **Mechanism Design** | Design rules so selfish behavior produces good outcomes | Create incentive structures, not mandates |
| **Vickrey Auction** | Second-price sealed bid; truthful bidding is dominant | Design systems where honesty is the best policy |
| **Dominant Strategy** | Strategy that is best regardless of others' actions | The "no-brainer" choice; mechanism design aims to make honesty dominant |

### Nash Equilibrium

```
         Player B
         Cooperate    Defect
Player A
Cooperate  (3,3)       (0,5)
Defect     (5,0)       (1,1)  ← Nash Equilibrium (Defect, Defect)

Both players defecting is stable — neither benefits from switching alone.
But (Cooperate, Cooperate) is better for both. This is the price of anarchy.
```

### Mechanism Design (Reverse Game Theory)

Rather than analyzing how players behave given rules, mechanism design asks: **what rules should we create so that rational self-interest produces the desired outcome?**

| Design Principle | Mechanism | Example |
|-----------------|-----------|---------|
| **Truthful revelation** | Vickrey (second-price) auction | Bidders bid their true value because overbidding risks overpaying, underbidding risks losing |
| **Aligned incentives** | Performance-based pay | Workers' self-interest aligns with organizational goals |
| **Reduced gaming** | Sealed bids | Prevent collusion and strategic posturing |
| **Dominant strategy truthfulness** | Strategy-proof mechanisms | No player benefits from lying, regardless of others' behavior |

### Price of Anarchy

Measures how much efficiency is lost when individuals act selfishly rather than cooperatively:

| Price of Anarchy | Interpretation |
|-----------------|---------------|
| **1.0** | Selfish behavior is as good as cooperation — perfect mechanism design |
| **1.0–1.5** | Minor efficiency loss; selfishness is nearly costless |
| **2.0+** | Significant loss; intervention (rules, coordination) is worth the overhead |
| **∞** | Total system failure under selfishness; cooperation is essential |

## Practical Applications

1. **Design for honesty**: Use Vickrey-style mechanisms so truthful behavior is dominant — don't rely on people being honest out of virtue
2. **Reduce the price of anarchy**: When selfish behavior creates large social costs, invest in coordination mechanisms
3. **Incentive alignment**: When people aren't behaving well, check incentives before blaming character
4. **Choice architecture as mechanism design**: [Choice architecture](term_choice_architecture.md) is mechanism design applied to decision environments

## Related Terms

### Decision Science
- **[Term: Choice Architecture](term_choice_architecture.md)** — Thaler & Sunstein's nudge theory IS mechanism design applied to human decisions
- **[Term: Computational Kindness](term_computational_kindness.md)** — Reducing cognitive burden is a form of cooperative game design
- **[Term: Information Cascades](term_information_cascades.md)** — Game-theoretic phenomenon where rational herding leads to irrational collective outcomes

### Cognitive Science
- **[Term: Cognitive Bias](term_cognitive_bias.md)** — Many biases arise from misapplied game-theoretic reasoning
- **[Term: Systems Thinking](term_systems_thinking.md)** — Game theory is systems thinking applied to strategic interaction

### Source
- **[Digest: Algorithms to Live By](../digest/digest_algorithms_to_live_by_christian.md)** — Chapter 11: Game Theory

## References

- Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 11: Game Theory. Henry Holt and Company.
- von Neumann, J. & Morgenstern, O. (1944). *Theory of Games and Economic Behavior*. Princeton University Press.
- Vickrey, W. (1961). "Counterspeculation, Auctions, and Competitive Sealed Tenders." *Journal of Finance*, 16(1), 8–37.
- Nisan, N. et al. (Eds.) (2007). *Algorithmic Game Theory*. Cambridge University Press.

---

**Last Updated**: March 12, 2026
**Status**: Active — Decision science, economics, and game theory
