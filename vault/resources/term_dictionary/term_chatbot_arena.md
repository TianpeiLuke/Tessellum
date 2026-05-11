---
tags:
  - resource
  - terminology
  - benchmarking
  - llm_evaluation
  - crowdsourcing
keywords:
  - Chatbot Arena
  - LMSYS
  - pairwise comparison
  - crowdsourced evaluation
  - LLM leaderboard
  - anonymous battle
  - Elo rating
  - human evaluation
  - model ranking
topics:
  - benchmarking
  - LLM evaluation
  - crowdsourcing
  - human-computer interaction
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Chatbot Arena

## Definition

**Chatbot Arena** is an open crowdsourced platform for evaluating large language models (LLMs) through **anonymous pairwise battles**. Users submit prompts and receive responses from two randomly selected anonymous models displayed side-by-side. After reading both responses, the user votes which is better (or declares a tie). These votes are aggregated using the **Elo rating system** to produce a continuous leaderboard ranking of participating LLMs. Launched by **LMSYS** (Large Model Systems Organization) at UC Berkeley in 2023, Chatbot Arena collected over 30,000 conversations in its initial deployment and has become a widely referenced benchmark for LLM quality.

## Full Name

Chatbot Arena (LMSYS Chatbot Arena, LMArena)

**Synonyms & Related Terms**:
- LMSYS Arena
- LLM Arena
- LMArena (rebranded name)
- Chatbot Arena Leaderboard

## Platform Design

### Core Principles

1. **Anonymous models**: Users do not know which models they are interacting with until after voting, eliminating brand bias
2. **Side-by-side comparison**: Both responses are displayed simultaneously, enabling direct quality comparison
3. **Free and open access**: No registration required; anyone can participate
4. **Diverse user prompts**: Users bring their own questions, producing ecologically valid evaluation data
5. **Continuous evaluation**: New models can be added to the pool at any time

### User Interaction Flow

```
User submits prompt
    → Prompt sent to two randomly selected anonymous models
    → Both responses displayed side-by-side
    → User votes: Model A wins | Model B wins | Tie | Both Bad
    → Model identities revealed
    → Elo ratings updated
```

### Model Pool

The arena maintains a pool of active models that evolves over time:
- Models are added as they become available (both proprietary and open-source)
- Early pool included: GPT-4, GPT-3.5-turbo, Claude-v1, Vicuna, Alpaca, LLaMA, Koala, Dolly, and others
- As of 2024-2025, the pool has expanded to include 70+ models from major providers and the open-source community
- Models may be retired or replaced as newer versions are released

## Elo Rating Computation

### Method

Each vote is treated as a match outcome in the Elo system:

- **Win for Model A**: $S_A = 1, S_B = 0$
- **Win for Model B**: $S_A = 0, S_B = 1$
- **Tie**: $S_A = 0.5, S_B = 0.5$

Ratings are updated after each vote:

$$R'_A = R_A + K(S_A - E_A)$$

where $E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$.

### Bootstrap Confidence Intervals

To address sensitivity to match ordering, Zheng et al. (2023) compute Elo ratings via **bootstrapping**:
1. Randomly sample votes with replacement
2. Compute Elo ratings from the bootstrap sample
3. Repeat 1000 times
4. Report median and 95% confidence intervals

This produces more stable rankings than a single pass through the data.

### Results from Initial Deployment

Chatbot Arena Elo rankings from the paper (approximately):

| Rank | Model | Elo Rating |
|:----:|-------|:----------:|
| 1 | GPT-4 | 1274 |
| 2 | Claude-v1 | 1224 |
| 3 | GPT-3.5-turbo | 1155 |
| 4 | Vicuna-13B | 1054 |
| 5 | Koala-13B | 980 |
| 6 | Alpaca-13B | 934 |
| 7 | LLaMA-13B | 854 |
| 8 | Dolly-12B | 835 |

## Data Collection and Quality

### Scale

- **Initial deployment**: 30,000+ conversations from anonymous users
- **Ongoing**: Continues to collect data; by 2024, over 1 million votes accumulated
- **Languages**: Primarily English, though multilingual prompts are accepted

### Data Cleaning

Zheng et al. (2023) describe several data quality measures:

1. **PII cleaning**: Personal identifiable information is detected and removed before public data release
2. **Toxic content flagging**: Conversations containing toxic or harmful content are flagged and excluded from public datasets
3. **Vote quality**: Obvious spam votes (e.g., voting within seconds of submission) can be filtered
4. **Duplicate detection**: Repeated prompts from the same user session are deduplicated

### Data Release

Cleaned conversation data has been released publicly for research purposes, enabling:
- Training of reward models and preference datasets
- Analysis of human evaluation patterns
- Development of improved evaluation methodologies

## Strengths

1. **Ecological validity**: Real users with real questions produce evaluation data that reflects genuine use cases — not researcher-designed test sets
2. **Continuous and scalable**: New models are added without redesigning the benchmark; the leaderboard updates in real time
3. **Diverse prompt coverage**: Thousands of unique user-generated prompts cover topics far broader than any fixed benchmark
4. **Eliminates brand bias**: Anonymous presentation forces evaluation based purely on response quality
5. **Low barrier to participation**: Free, no registration — accessible to a global audience
6. **Community trust**: Has become the de facto industry standard for LLM ranking, referenced in model release announcements

## Limitations

1. **Selection bias in user base**: Users who find and use the platform are likely technically sophisticated and English-speaking, not representative of the general population
2. **English-centric**: Most conversations are in English, limiting assessment of multilingual capabilities
3. **Pool sensitivity of Elo ratings**: Adding or removing models changes the competitive landscape, making historical Elo comparisons across different pool compositions unreliable
4. **Prompt distribution shift**: User prompts evolve over time as the platform gains popularity and different user communities join
5. **No category-level granularity**: Unlike MT-Bench, Chatbot Arena produces a single overall ranking without per-category breakdowns (though later analysis has added category tags)
6. **Tie handling**: Users may default to "tie" when differences are subtle, diluting signal
7. **Latency and cost not captured**: The ranking reflects only response quality, not inference speed or cost — important factors for deployment decisions

## Evolution: Chatbot Arena 2.0

Subsequent work (Chiang et al., 2024) introduced improvements:
- **Style-controlled evaluation**: Separating style (length, formatting) from substance in rankings
- **Category tagging**: Automatic classification of prompts into categories for per-domain analysis
- **Expanded model pool**: 70+ models from diverse providers
- **Multilingual analysis**: Breakdown of performance by prompt language
- **Statistical improvements**: Transition from online Elo to Bradley-Terry MLE for more stable rankings

## Chatbot Arena vs. MT-Bench

| Aspect | Chatbot Arena | MT-Bench |
|--------|---------------|----------|
| **Evaluator** | Real users (crowdsourced) | GPT-4 (automated) |
| **Questions** | User-generated (open) | Fixed 80 questions |
| **Scale** | 30K+ votes (growing) | 80 questions (static) |
| **Format** | Pairwise comparison | Single-answer grading (1-10) |
| **Ranking** | Elo ratings | Mean scores |
| **Cost** | Free (volunteer users) | API costs for GPT-4 |
| **Category analysis** | No (initially) | Yes (8 categories) |
| **Reproducibility** | Non-deterministic (user variation) | Deterministic (fixed questions + judge) |
| **Correlation** | — | Spearman $\rho > 0.9$ between the two |

The two approaches are complementary: MT-Bench provides controlled, reproducible evaluation while Chatbot Arena provides ecologically valid evaluation at scale.

## Related Terms

- **[Elo Rating](term_elo_rating.md)**: The ranking algorithm used to convert pairwise votes into model rankings
- **[LLM-as-a-Judge](term_llm_as_a_judge.md)**: Automated alternative to human evaluation; validated against Chatbot Arena rankings
- **[MT-Bench](term_mt_bench.md)**: Controlled benchmark companion to Chatbot Arena; high correlation between their rankings
- **[RLHF](term_rlhf.md)**: Training methodology that uses similar pairwise preference data to what Chatbot Arena collects
- **[Position Bias](term_position_bias.md)**: Side-by-side display may introduce position effects, though user evaluation is less susceptible than LLM judges

## References

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)](../papers/lit_zheng2023judging.md) — Introduces Chatbot Arena and validates it alongside MT-Bench
- Chiang et al. (2024). "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference" — Extended analysis and improvements (Chatbot Arena 2.0)
- Elo, A. (1978). *The Rating of Chessplayers, Past and Present* — The rating system used for ranking

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Chatbot Arena (LMSYS Chatbot Arena) |
| **Launched By** | LMSYS, UC Berkeley (2023) |
| **Evaluation Type** | Crowdsourced anonymous pairwise battles |
| **Ranking Method** | Elo rating system with bootstrap confidence intervals |
| **Scale** | 30K+ votes initially; 1M+ by 2024 |
| **Key Innovation** | Ecologically valid, continuous LLM evaluation from real user preferences |
| **Correlation with MT-Bench** | Spearman $\rho > 0.9$ |
| **Limitation** | Selection bias, English-centric, pool-sensitive Elo ratings |

---

**Last Updated**: March 8, 2026
**Status**: Active
