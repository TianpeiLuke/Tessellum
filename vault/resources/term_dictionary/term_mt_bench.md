---
tags:
  - resource
  - terminology
  - benchmarking
  - llm_evaluation
keywords:
  - MT-Bench
  - multi-turn benchmark
  - LLM evaluation
  - chat assistant evaluation
  - GPT-4 judge
  - single-answer grading
  - pairwise comparison
  - open-ended evaluation
topics:
  - benchmarking
  - LLM evaluation
  - natural language processing
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: MT-Bench

## Definition

**MT-Bench** (Multi-Turn Benchmark) is a benchmark for evaluating LLM chat assistants, introduced by Zheng et al. (2023). It consists of **80 multi-turn questions** spanning **8 categories**, where each question includes an initial prompt and a follow-up turn designed to test instruction-following, multi-turn coherence, and domain knowledge. Responses are evaluated by a strong LLM judge (primarily GPT-4) using **single-answer grading** on a 1-10 scale. MT-Bench was specifically designed to differentiate among strong chat models that perform similarly on traditional benchmarks like MMLU or HellaSwag.

## Full Name

MT-Bench (Multi-Turn Benchmark)

**Synonyms & Related Terms**:
- Multi-Turn Benchmark
- LMSYS MT-Bench
- LLM Chat Benchmark

## Design Principles

### Why MT-Bench Was Needed

Traditional benchmarks (MMLU, HellaSwag, HumanEval) rely on closed-ended questions with single correct answers and evaluate primarily factual knowledge or narrow skills. They fail to differentiate among instruction-tuned chat models that have converged in factual accuracy but differ substantially in conversational quality. MT-Bench addresses this gap through:

1. **Open-ended questions**: Require generation, not selection from options
2. **Multi-turn structure**: Tests ability to maintain context and follow up on prior conversation
3. **Diverse categories**: Covers both knowledge-intensive and creative tasks
4. **Automated judging**: Uses LLM-as-a-Judge for scalable evaluation of open-ended responses

### The 8 Categories

| Category | Example Topic | Tests |
|----------|---------------|-------|
| **Writing** | Creative writing, editing, style | Creativity, fluency, instruction adherence |
| **Roleplay** | Character simulation, scenario acting | Consistency, persona maintenance |
| **Reasoning** | Logical puzzles, analogies | Logical consistency, chain of thought |
| **Math** | Word problems, calculations | Numerical accuracy, step-by-step reasoning |
| **Coding** | Algorithm implementation, debugging | Code correctness, explanation quality |
| **Extraction** | Information extraction, summarization | Precision, format compliance |
| **STEM** | Science, technology, engineering | Domain knowledge, accurate explanation |
| **Humanities** | History, philosophy, social sciences | Nuanced understanding, argumentation |

Each category contains **10 questions** (80 total), with each question having **2 turns** (160 total model responses to evaluate).

### Multi-Turn Structure

Each MT-Bench question consists of:
- **Turn 1**: An initial question or task (e.g., "Write a persuasive essay about remote work")
- **Turn 2**: A follow-up that builds on Turn 1 (e.g., "Now rewrite the essay to take the opposing position")

The follow-up turn is designed to test:
- **Instruction following**: Can the model correctly interpret and execute the modification?
- **Context retention**: Does the model remember and reference its Turn 1 response?
- **Flexibility**: Can the model adjust its output based on new constraints?

## Scoring Methodology

### Primary Mode: Single-Answer Grading

The default evaluation mode uses GPT-4 as a judge:

1. The model's response is presented to GPT-4 along with the question
2. GPT-4 assigns a score from 1 to 10 with a detailed justification
3. Scores are averaged across all 80 questions for an overall MT-Bench score
4. Per-category scores can be computed (average of 10 questions per category)

**Typical Score Ranges** (from Zheng et al., 2023):

| Model | MT-Bench Score |
|-------|:--------------:|
| GPT-4 | 8.99 |
| Claude-v1 | 7.90 |
| GPT-3.5-turbo | 7.94 |
| Vicuna-13B | 6.57 |
| Alpaca-13B | 4.53 |
| LLaMA-13B | 2.61 |

### Alternative Mode: Pairwise Comparison

MT-Bench also supports pairwise comparison grading:
- Two model responses are presented side-by-side
- The judge selects which response is better (or tie)
- Results can be aggregated into Elo ratings or win rates

### Agreement with Human Judges

Zheng et al. (2023) found that GPT-4 single-answer grading on MT-Bench achieves:
- **>80% agreement** with human preferences (matching the level of inter-human agreement)
- **Strong correlation** with Chatbot Arena Elo ratings (Spearman $\rho > 0.9$)

## Comparison to Other Benchmarks

| Benchmark | Type | Questions | Evaluation | Multi-Turn | Open-Ended |
|-----------|------|:---------:|------------|:----------:|:----------:|
| **MT-Bench** | Chat quality | 80 | LLM judge (1-10) | Yes | Yes |
| **MMLU** | Knowledge | 14K+ | Multiple choice | No | No |
| **HellaSwag** | Commonsense | 10K | Multiple choice | No | No |
| **HumanEval** | Coding | 164 | Pass@k | No | Partially |
| **Alpaca Eval** | Instruction following | 805 | LLM pairwise vs. ref | No | Yes |
| **Chatbot Arena** | Overall quality | Continuous | Human pairwise | Yes | Yes |

### Key Differentiators

1. **Multi-turn**: Unlike most benchmarks, MT-Bench explicitly tests conversational ability across turns
2. **Category diversity**: Covers 8 distinct capability domains in a single benchmark
3. **Discriminative for strong models**: Designed to separate GPT-4-class models from each other, not just from weak baselines
4. **Compact**: Only 80 questions, making evaluation fast and cost-effective

## Strengths

1. **Multi-turn evaluation**: Captures conversational dynamics that single-turn benchmarks miss
2. **Open-ended format**: Evaluates generation quality, not just factual recall
3. **High correlation with human judgment**: MT-Bench scores track Chatbot Arena rankings closely
4. **Category-level diagnostics**: Per-category scores reveal specific model strengths and weaknesses
5. **Reproducible**: Fixed question set with automated judging enables consistent comparison
6. **Efficient**: 80 questions are sufficient to produce stable, discriminative rankings

## Limitations

1. **Small question set**: 80 questions (10 per category) may not fully represent each domain; individual question quality has outsized impact
2. **GPT-4 dependency**: Evaluation quality is bounded by GPT-4's judgment capability; may disadvantage models with different strengths
3. **Category balance**: Equal weighting of 8 categories may not reflect real-world usage patterns
4. **Static benchmark**: Fixed questions can be memorized or gamed by models trained after publication
5. **English-only**: Does not assess multilingual capabilities
6. **Ceiling effects**: As models improve beyond GPT-4, the judge may not discriminate effectively at the top

## Related Terms

- **[LLM-as-a-Judge](term_llm_as_a_judge.md)**: The evaluation paradigm that MT-Bench relies on for automated scoring
- **[Elo Rating](term_elo_rating.md)**: Alternative ranking method used in Chatbot Arena; MT-Bench scores correlate with Elo ratings
- **[Chatbot Arena](term_chatbot_arena.md)**: Crowdsourced evaluation platform; MT-Bench serves as its controlled counterpart
- **[RLHF](term_rlhf.md)**: Training methodology that produces the aligned models MT-Bench is designed to evaluate
- **[Position Bias](term_position_bias.md)**: A bias that affects pairwise comparison mode of MT-Bench evaluation

## References

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)](../papers/lit_zheng2023judging.md) — Introduces MT-Bench and validates LLM-as-a-Judge evaluation
- Hendrycks et al. (2021). "Measuring Massive Multitask Language Understanding" — MMLU benchmark for comparison
- Li et al. (2023). "AlpacaEval: An Automatic Evaluator of Instruction-following Models" — Alternative LLM-judged benchmark

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | MT-Bench (Multi-Turn Benchmark) |
| **Introduced By** | Zheng et al. (2023), LMSYS / UC Berkeley |
| **Size** | 80 questions, 2 turns each, 8 categories |
| **Evaluation** | GPT-4 single-answer grading (1-10 scale) |
| **Key Innovation** | Multi-turn, open-ended evaluation that differentiates strong chat models |
| **Human Agreement** | >80% agreement with human preferences |
| **Correlation** | Spearman $\rho > 0.9$ with Chatbot Arena Elo ratings |
| **Limitation** | Small size, GPT-4 dependency, English-only |

---

**Last Updated**: March 8, 2026
**Status**: Active
