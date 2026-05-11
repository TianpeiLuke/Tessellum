---
tags:
  - resource
  - terminology
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
  - program synthesis
  - LLM systems
topics:
  - LLM Systems
  - Automated Program Optimization
  - Agentic AI
language: markdown
date of note: 2026-04-02
status: active
building_block: concept
---

# Meta-Harness

## Definition

**Meta-Harness** is an automated harness engineering system (Lee et al., 2026) that optimizes the **entire code infrastructure wrapping an LLM** — what information to store, retrieve, and present to the model — not just prompts. A **model harness** is the code layer managing context windows, retrieval strategies, state tracking, tool calls, and output parsing. Meta-Harness uses an **agentic proposer** (Claude Code Opus-4.6) that browses a filesystem of prior candidates' source code, evaluation scores, and raw execution traces to generate improved harness code.

The key insight: prior text optimizers (DSPy, TextGrad, OPRO) compress feedback too aggressively (scalar scores, brief summaries), losing diagnostic information about *why* candidates fail. Meta-Harness provides **10M tokens of accessible information per iteration** — 500–5,000× more than prior methods — enabling root-cause diagnosis of failures through raw execution trace inspection.

## Key Properties

- **Harness > prompt**: Optimizes the entire wrapping code (retrieval, context management, state, tools), not just prompt text — a superset of prompt optimization
- **Agentic proposer**: Claude Code Opus-4.6 browses filesystem selectively (median 82 files/iteration: 41% source, 40% traces, 6% scores)
- **Rich feedback**: Raw execution traces preserve causal diagnostic signal; summaries compress it away (ablation: traces 50.0 median vs summaries 34.9)
- **Interpretable output**: Discovered harnesses are readable Python code — auditable and manually improvable
- **Cross-model transfer**: Harness discovered on one model transfers to 5 held-out models (+4.7 points average)
- **Three domains validated**: Text classification (+7.7 pts, 4× fewer tokens), IMO-level math (+4.7 pts), agentic coding (#2 on TerminalBench-2)

## Applications

| Domain | Application | Key Result |
|--------|-------------|------------|
| **Text classification** | Online few-shot with 215+ classes | +7.7 pts over ACE, 4× fewer tokens |
| **Math reasoning** | RAG-augmented IMO-level problems | +4.7 pts across 5 held-out models |
| **Agentic coding** | TerminalBench-2 autonomous tasks | #2 on leaderboard (76.4%) |
| **Abuse prevention** | Potential: optimize investigation skills (question generation, SOP matching) | Not yet applied |

## Related Terms

- **[LLM](term_llm.md)**: The model being harnessed; Meta-Harness optimizes the code wrapping it
- **[RAG](term_rag.md)**: RAG is one type of harness pattern; Meta-Harness discovers better retrieval strategies
- **[Information Retrieval](term_information_retrieval.md)**: Retrieval strategy is a key harness component optimized by Meta-Harness
- **[ANN Search](term_ann_search.md)**: ANN indices power the retrieval component that Meta-Harness can optimize
- **[Phi](term_phi.md)**: Efficient LLMs that benefit from harness optimization (compact models + good harness = frontier performance)
- **[Foundation Model](term_foundation_model.md)**: Meta-Harness treats the LLM as a frozen foundation and optimizes the wrapping code

## References

### Vault Sources

- [Meta-Harness Literature Note](../papers/lit_lee2026metaharness.md) — Full paper digest with section notes
- [Meta-Harness Review](../papers/review_lee2026metaharness.md) — OpenReview-style evaluation (Overall 8/10)

### External Sources

- [Lee et al. (2026). "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv:2603.28052](https://arxiv.org/abs/2603.28052) — Original paper
