---
tags:
  - resource
  - literature_note
  - llm_evaluation
  - benchmarking
  - human_preference_alignment
keywords:
  - LLM-as-a-Judge
  - MT-Bench
  - Chatbot Arena
  - position bias
  - verbosity bias
  - self-enhancement bias
  - pairwise comparison
  - Elo rating
  - human preference
  - model evaluation
topics:
  - LLM Evaluation
  - Benchmarking
  - Human Preference Alignment
domain: "LLM Evaluation"
language: markdown
date of note: 2026-03-08
paper_title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
authors:
  - Lianmin Zheng
  - Wei-Lin Chiang
  - Ying Sheng
  - Siyuan Zhuang
  - Zhanghao Wu
  - Yonghao Zhuang
  - Zi Lin
  - Zhuohan Li
  - Dacheng Li
  - Eric P. Xing
  - Hao Zhang
  - Joseph E. Gonzalez
  - Ion Stoica
year: 2023
source: "arXiv:2306.05685"
venue: "NeurIPS 2023"
DOI: "10.52202/075280-2020"
arXiv: "2306.05685"
semantic_scholar_id: "a0a79dad89857a96f8f71b14238e5237cbfc4787"
zotero_key: "53U4D2GX"
paper_id: zheng2023judging
paper_notes:
  - paper_zheng2023judging_intro.md
  - paper_zheng2023judging_contrib.md
  - paper_zheng2023judging_algo.md
  - paper_zheng2023judging_exp_design.md
  - paper_zheng2023judging_exp_result.md
status: active
building_block: hypothesis
---

# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena |
| **Authors** | Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica |
| **Year** | 2023 |
| **Venue** | NeurIPS 2023 |
| **arXiv** | [2306.05685](https://arxiv.org/abs/2306.05685) |
| **Semantic Scholar** | [a0a79dad89...](https://www.semanticscholar.org/paper/a0a79dad89857a96f8f71b14238e5237cbfc4787) |
| **Zotero** | 53U4D2GX |
| **Citations** | ~7,279 |

## Abstract

Evaluating large language model (LLM) based chat assistants is challenging due to their broad capabilities and the inadequacy of existing benchmarks in measuring human preferences. To address this, we explore using strong LLMs as judges to evaluate these models on more open-ended questions. We examine the usage and limitations of LLM-as-a-judge, including position, verbosity, and self-enhancement biases, as well as limited reasoning ability, and propose solutions to mitigate some of them. We then verify the agreement between LLM judges and human preferences by introducing two benchmarks: MT-bench, a multi-turn question set; and Chatbot Arena, a crowdsourced battle platform. Our results reveal that strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans. Hence, LLM-as-a-judge is a scalable and explainable way to approximate human preferences, which are otherwise very expensive to obtain. Additionally, we show our benchmark and traditional benchmarks complement each other by evaluating several variants of LLaMA and Vicuna. The MT-bench questions, 3K expert votes, and 30K conversations with human preferences are publicly available at https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_zheng2023judging_intro](paper_zheng2023judging_intro.md) | Benchmark inadequacy for aligned models; need for human preference evaluation; three categories of existing benchmarks |
| **Contribution** | [paper_zheng2023judging_contrib](paper_zheng2023judging_contrib.md) | Systematic study of LLM-as-a-judge; MT-bench (80 multi-turn questions, 8 categories); Chatbot Arena (30K crowdsourced votes); hybrid evaluation framework |
| **Method** | [paper_zheng2023judging_algo](paper_zheng2023judging_algo.md) | Three judge types (pairwise, single-answer, reference-guided); bias analysis (position, verbosity, self-enhancement); mitigation strategies (swap, few-shot, CoT, reference) |
| **Experiment Design** | [paper_zheng2023judging_exp_design](paper_zheng2023judging_exp_design.md) | 6 models on MT-bench; 58 expert labelers; 3K arena votes; agreement metrics with and without ties |
| **Experiment Results** | [paper_zheng2023judging_exp_result](paper_zheng2023judging_exp_result.md) | GPT-4 judge achieves >80% agreement with humans (matching human-human agreement at 81%); single-answer grading nearly matches pairwise; hybrid benchmarks complement traditional metrics |
| **Review** | [review_zheng2023judging](review_zheng2023judging.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (4 review lenses applied) |

## Summary

- **Background**: Existing LLM benchmarks like MMLU and HELM focus on closed-ended, core-capability tasks and fail to capture the human preference differences between aligned chat models and their base models, creating a fundamental evaluation gap. <!-- VERIFY: problem statement -->
- **Contribution**: The paper introduces LLM-as-a-judge as a systematic evaluation paradigm, along with two complementary benchmarks -- MT-bench (80 multi-turn questions across 8 categories) and Chatbot Arena (a crowdsourced anonymous battle platform with 30K votes) -- and identifies three key biases (position, verbosity, self-enhancement) with practical mitigations.
- **Method**: Three LLM judge variations are proposed -- pairwise comparison, single-answer grading, and reference-guided grading -- with bias mitigation strategies including position swapping, few-shot prompting, chain-of-thought reasoning, and reference-guided judging that reduces math grading failure from 70% to 15%. <!-- VERIFY: method details -->
- **Results**: GPT-4 as a judge achieves over 80% agreement with human preferences on both MT-bench and Chatbot Arena, matching the 81% human-human agreement rate; single-answer grading closely tracks pairwise comparison, and the proposed benchmarks complement traditional capability benchmarks by revealing alignment differences invisible to MMLU-style evaluation. <!-- VERIFY: exact numbers -->

## Relevance to Our Work

- **[LLM-as-a-Judge](../term_dictionary/term_llm_as_a_judge.md)**: This paper defines and systematically studies the LLM-as-a-judge paradigm, establishing it as a scalable alternative to human evaluation
- **[Reward Model](../term_dictionary/term_reward_model.md)**: The pairwise comparison framework connects to Bradley-Terry preference models used in reward modeling for RLHF
- **[RLHF](../term_dictionary/term_rlhf.md)**: The paper contextualizes LLM-as-a-judge within the broader alignment pipeline, where human preference data drives model training
- **[Constitutional AI](../term_dictionary/term_constitutional_ai.md)**: Alternative alignment approaches that also leverage AI-generated feedback for evaluation
- **[DPO](../term_dictionary/term_dpo.md)**: Preference optimization methods that benefit from scalable preference data generation enabled by LLM judges

## Related Documentation

### Paper Notes
- [Introduction](paper_zheng2023judging_intro.md)
- [Contribution](paper_zheng2023judging_contrib.md)
- [Method](paper_zheng2023judging_method.md)
- [Experiment Design](paper_zheng2023judging_exp_design.md)
- [Experiment Results](paper_zheng2023judging_exp_result.md)

### Related Vault Notes
- [LLM-as-a-Judge](../term_dictionary/term_llm_as_a_judge.md) — Primary concept defined and studied in this paper
- [Reward Model](../term_dictionary/term_reward_model.md) — Bradley-Terry preference framework underlying pairwise comparison
- [RLHF](../term_dictionary/term_rlhf.md) — Alignment context; human preference data for model training
- [Constitutional AI](../term_dictionary/term_constitutional_ai.md) — Alternative alignment method using AI feedback
- [DPO](../term_dictionary/term_dpo.md) — Preference optimization benefiting from scalable LLM judge data

### Related Literature
- Ouyang et al. (2022). "Training language models to follow instructions with human feedback" — [lit_ouyang2022training](lit_ouyang2022training.md)
- Bai et al. (2022). "Constitutional AI: Harmlessness from AI Feedback" — [lit_bai2022constitutional](lit_bai2022constitutional.md)
- Brown et al. (2020). "Language Models are Few-Shot Learners" — [lit_brown2020language](lit_brown2020language.md)
- Touvron et al. (2023). "LLaMA: Open and Efficient Foundation Language Models" — [lit_touvron2023llama](lit_touvron2023llama.md)
- Chiang et al. (2023). "Vicuna: An Open-Source Chatbot Impressing GPT-4 with 90%* ChatGPT Quality"
