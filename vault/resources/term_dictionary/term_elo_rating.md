---
tags:
  - resource
  - terminology
  - statistics
  - evaluation
  - llm_evaluation
keywords:
  - Elo rating
  - Elo score
  - Bradley-Terry model
  - pairwise comparison
  - ranking system
  - K-factor
  - expected score
  - Chatbot Arena
  - chess rating
topics:
  - statistics
  - evaluation methodology
  - LLM evaluation
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Elo Rating System

## Definition

The **Elo rating system** is a method for calculating the relative skill levels of players in zero-sum games, originally developed by Arpad Elo (1960) for chess. Each player (or model) is assigned a numerical rating $R$, and the expected outcome of a match between two players is computed via the **Bradley-Terry model**:

$$P(A \text{ beats } B) = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$

After each match, ratings are updated according to the observed outcome $S_A$ (1 for win, 0.5 for draw, 0 for loss) versus the expected score $E_A$:

$$R'_A = R_A + K \cdot (S_A - E_A)$$

where $K$ is the update magnitude (K-factor). In the context of LLM evaluation, the Elo rating system was adopted by **Chatbot Arena** (Zheng et al., 2023) to rank language models from crowdsourced pairwise human preference votes, producing a continuous-valued leaderboard that reflects relative model quality.

## Full Name

Elo Rating System (Elo Score, Elo Ranking)

**Synonyms & Related Terms**:
- Bradley-Terry Rating (the underlying probabilistic model)
- Glicko / Glicko-2 (extensions with rating uncertainty)
- TrueSkill (Microsoft's Bayesian generalization)
- Arena Score (Elo rating as applied in Chatbot Arena)

## Mathematical Formulation

### Bradley-Terry Model

The Elo system is a special case of the Bradley-Terry model (1952). Given two players $A$ and $B$ with strengths $\gamma_A$ and $\gamma_B$:

$$P(A > B) = \frac{\gamma_A}{\gamma_A + \gamma_B}$$

Setting $\gamma_i = 10^{R_i / 400}$ recovers the Elo formula. The logistic form means a 400-point rating difference corresponds to a 10:1 expected win ratio.

### Rating Updates

After observing outcome $S_A \in \{0, 0.5, 1\}$:

1. **Expected score**: $E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$
2. **Update**: $R'_A = R_A + K(S_A - E_A)$
3. **Symmetry**: $R'_B = R_B + K(S_B - E_B)$ where $S_B = 1 - S_A$

The system is **zero-sum** — the total rating points in the pool are conserved (ignoring draws in some implementations).

### K-Factor

The K-factor controls update sensitivity:

| Context | Typical $K$ | Effect |
|---------|:-----------:|--------|
| FIDE Chess (new players) | 40 | Fast adaptation |
| FIDE Chess (established) | 20 | Moderate stability |
| FIDE Chess (elite, $R > 2400$) | 10 | High stability |
| Chatbot Arena | 4-32 | Varies by implementation; lower $K$ for stability |

Higher $K$ produces faster convergence but more volatile ratings. Lower $K$ produces stable ratings but requires more matches to converge.

## Properties

### Strengths

1. **Simplicity**: Only requires pairwise win/loss outcomes — no absolute scoring rubric needed
2. **Interpretability**: Rating differences map directly to win probabilities (e.g., +200 points $\approx$ 76% win rate)
3. **Self-calibrating**: Ratings automatically adjust as more matches are observed
4. **Ordinal ranking from pairwise data**: Converts pairwise comparisons into a global ranking without requiring a full comparison matrix
5. **Battle-tested**: Decades of successful use in chess, Go, online gaming, and now AI evaluation

### Limitations

1. **Non-transitivity**: If $A$ beats $B$ and $B$ beats $C$, it does not guarantee $A$ beats $C$. Elo assumes a one-dimensional skill axis, but LLM quality is multidimensional (coding, reasoning, creativity, etc.)
2. **Pool sensitivity**: Ratings depend on the population of competitors. Adding or removing models can shift existing ratings, making historical comparisons unreliable
3. **Order dependence**: Final ratings depend on the sequence of matches, though this diminishes with more games
4. **No uncertainty quantification**: Standard Elo provides a point estimate without confidence intervals (addressed by Glicko/TrueSkill)
5. **Assumes stationarity**: Ratings assume constant player skill, but LLMs may be updated or fine-tuned over time

## Use in LLM Evaluation

### Chatbot Arena

Zheng et al. (2023) adapted Elo ratings for LLM evaluation in Chatbot Arena:

- Users submit prompts and receive responses from two anonymous models side-by-side
- Users vote which response is better (or tie)
- Each vote is treated as a match outcome and Elo ratings are updated
- After 30K+ votes, stable rankings emerge

### Elo vs. Other Ranking Methods

| Method | Input | Output | Key Difference |
|--------|-------|--------|----------------|
| **Elo Rating** | Pairwise votes | Scalar rating per model | Online updates, simple |
| **Bradley-Terry MLE** | Pairwise votes | Strength parameters | Batch estimation, principled |
| **Win Rate Matrix** | Pairwise votes | $n \times n$ win-rate table | No single ranking, full information |
| **Single-Answer Grading** | Absolute scores | Mean score per model | No pairwise comparison needed |

### Results from Zheng et al. (2023)

The Chatbot Arena Elo leaderboard (as of the paper) showed:

| Model | Elo Rating (approx.) |
|-------|:-------------------:|
| GPT-4 | 1274 |
| Claude-v1 | 1224 |
| GPT-3.5-turbo | 1155 |
| Vicuna-13B | 1054 |
| Alpaca-13B | 934 |

These Elo ratings showed strong agreement with MT-Bench scores (Spearman correlation > 0.9), validating both evaluation approaches.

## Related Terms

- **[LLM-as-a-Judge](term_llm_as_a_judge.md)**: LLM judges produce pairwise preferences that can feed into Elo computation
- **[Reward Model](term_reward_model.md)**: Often trained on Bradley-Terry objectives — the same probabilistic model underlying Elo
- **[RLHF](term_rlhf.md)**: Uses pairwise preference data similar to Elo match outcomes for reward model training
- **[Chatbot Arena](term_chatbot_arena.md)**: The primary platform using Elo ratings for LLM evaluation
- **[MT-Bench](term_mt_bench.md)**: Benchmark whose scores correlate strongly with Chatbot Arena Elo ratings
- **[Position Bias](term_position_bias.md)**: Can introduce systematic errors into pairwise comparisons that feed Elo computation

## References

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)](../papers/lit_zheng2023judging.md) — Adapted Elo rating for LLM evaluation via Chatbot Arena
- Elo, A. (1978). *The Rating of Chessplayers, Past and Present*. Arco Publishing — Original Elo rating system
- Bradley, R. A. & Terry, M. E. (1952). "Rank Analysis of Incomplete Block Designs: The Method of Paired Comparisons" — Underlying probabilistic model
- Glickman, M. E. (1999). "Parameter Estimation in Large Dynamic Paired Comparison Experiments" — Glicko rating system with uncertainty

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Elo Rating System |
| **Invented By** | Arpad Elo (1960), for chess |
| **Core Formula** | $P(A > B) = 1/(1 + 10^{(R_B - R_A)/400})$ |
| **Update Rule** | $R'_A = R_A + K(S_A - E_A)$ |
| **Key Property** | Converts pairwise outcomes into global scalar rankings |
| **LLM Application** | Chatbot Arena leaderboard for crowdsourced LLM evaluation |
| **Key Limitation** | Assumes one-dimensional skill; LLM quality is multidimensional |
| **Extensions** | Glicko (uncertainty), TrueSkill (Bayesian), Bradley-Terry MLE (batch) |

---

**Last Updated**: March 8, 2026
**Status**: Active
