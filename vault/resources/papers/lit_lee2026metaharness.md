---
tags:
  - resource
  - papers
  - literature_note
  - llm
  - agentic_ai
  - program_synthesis
  - optimization
  - prompt_engineering
keywords:
  - Meta-Harness
  - model harness
  - harness engineering
  - outer-loop optimization
  - agentic proposer
  - execution traces
  - context engineering
  - DSPy
  - TextGrad
  - program synthesis
topics:
  - LLM Systems
  - Automated Program Optimization
  - Agentic AI
  - Prompt Engineering
language: markdown
date of note: 2026-04-02
status: active
building_block: hypothesis
paper_id: lee2026metaharness
arxiv_id: "2603.28052"
doi: "10.48550/arXiv.2603.28052"
citation_count: 0
year: 2026
venue: arXiv
paper_notes:
  - paper_lee2026metaharness_intro.md
  - paper_lee2026metaharness_contrib.md
  - paper_lee2026metaharness_algo.md
  - paper_lee2026metaharness_exp_design.md
  - paper_lee2026metaharness_exp_result.md
---

# Literature Note: Meta-Harness — End-to-End Optimization of Model Harnesses

## Citation

Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O., & Finn, C. (2026). "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv:2603.28052.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_lee2026metaharness_intro](paper_lee2026metaharness_intro.md) | Harness = code wrapping LLM; manual design bottleneck; prior optimizers too compressed |
| **Contributions** | [paper_lee2026metaharness_contrib](paper_lee2026metaharness_contrib.md) | Outer-loop search over harness code; agentic proposer with filesystem; 3 domains |
| **Algorithm** | [paper_lee2026metaharness_algo](paper_lee2026metaharness_algo.md) | Proposer architecture, filesystem interface, Pareto selection, 10M tokens/iteration |
| **Experiment Design** | [paper_lee2026metaharness_exp_design](paper_lee2026metaharness_exp_design.md) | Text classification, RAG math, agentic coding benchmarks |
| **Experiment Results** | [paper_lee2026metaharness_exp_result](paper_lee2026metaharness_exp_result.md) | +7.7 on classification (4× fewer tokens), +4.7 on IMO math, #2 on TerminalBench-2 |
| **Review** | [review_lee2026metaharness](review_lee2026metaharness.md) | OpenReview-style evaluation; 5 strengths, 4 weaknesses, 6 questions (5 review lenses applied) |

## Core Idea

**Meta-Harness** introduces the concept of automated **harness engineering** — optimizing not just prompts or model weights, but the entire code infrastructure that wraps an LLM (what to store, retrieve, and present). The system uses an **agentic proposer** (Claude Code Opus-4.6) that reads source code, evaluation scores, and raw execution traces from a filesystem to generate improved harness code candidates. Unlike prior text optimizers (DSPy, TextGrad, OPRO) that compress feedback to scalar scores or brief summaries, Meta-Harness provides the proposer with **10M tokens per iteration** of rich diagnostic information — orders of magnitude more context than prior methods.

The key insight: **harness behavior has long-horizon dependencies** — early design choices (retrieval strategy, context management, state updates) affect reasoning steps far downstream, and compressed summaries lose the causal links needed to diagnose failures.

## Key Takeaways

1. **Harness > prompt**: LLM performance depends as much on the wrapping code (harness) as on the model itself — optimizing the harness yields larger gains than prompt tuning alone
2. **Rich feedback >> compressed feedback**: The agentic proposer reads 82 files per iteration (41% source code, 40% traces) — raw traces preserve diagnostic signal that summaries destroy
3. **Filesystem as optimization memory**: Prior candidates' code + scores + traces are stored in a filesystem the proposer can freely browse — making optimization history inspectable and searchable
4. **Transfer across models**: A single harness discovered on one model (GPT-OSS-20B) improves accuracy by 4.7 points on average across 5 held-out models — harness quality transfers
5. **Discovered strategies are interpretable**: Draft-Verification for classification, four-route BM25 router for math, environment bootstrapping for coding — all human-readable and auditable
6. **Claude Code as proposer**: The system itself runs Claude Code (Opus-4.6) as the harness proposer — demonstrating Claude's capability as an automated code optimization agent

## Relevance to Abuse Slipbox

Meta-Harness directly connects to the Abuse Slipbox's skill architecture:
- **Skills as harnesses**: Each Claude/Kiro skill is a harness — code that wraps an LLM to perform a specific task (search, digest, review, etc.)
- **Skill optimization opportunity**: Meta-Harness suggests that automated optimization of skill code (not just prompts) could improve performance — e.g., optimizing the paper review skill's question generation or the term capture skill's web search strategy
- **Filesystem-as-memory**: The Abuse Slipbox already uses a filesystem (vault notes + database) as persistent memory for LLM interactions — Meta-Harness formalizes this pattern
- **Execution traces**: The Slipbox's skill pipeline could log execution traces to enable Meta-Harness-style optimization across skill invocations

## Related Notes

- [Term: LLM](../term_dictionary/term_llm.md) — The model being harnessed
- [Term: RAG](../term_dictionary/term_rag.md) — RAG is one type of harness pattern; Meta-Harness optimizes it
- [Term: Phi](../term_dictionary/term_phi.md) — Efficient LLMs as candidates for harness optimization
- [Term: Information Retrieval](../term_dictionary/term_information_retrieval.md) — Retrieval is a key harness component optimized by Meta-Harness

---

**Last Updated**: 2026-04-02
