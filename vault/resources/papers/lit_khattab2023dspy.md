---
tags:
  - resource
  - papers
  - literature_note
  - llm
  - agentic_ai
  - program_synthesis
  - prompt_engineering
  - composable_modules
keywords:
  - DSPy
  - declarative LM programming
  - signatures
  - modules
  - teleprompters
  - optimizers
  - composable pipeline
  - self-improving
  - compilation
  - prompt optimization
topics:
  - LLM Systems
  - Program Synthesis
  - Prompt Engineering
  - Agentic AI
language: markdown
date of note: 2026-04-10
status: active
building_block: hypothesis
paper_id: khattab2023dspy
arxiv_id: "2310.03714"
doi: ""
citation_count: 634
year: 2023
venue: ICLR 2024
paper_notes:
  - paper_khattab2023dspy_intro.md
  - paper_khattab2023dspy_contrib.md
  - paper_khattab2023dspy_algo.md
  - paper_khattab2023dspy_exp_design.md
  - paper_khattab2023dspy_exp_result.md
---

# Literature Note: DSPy — Compiling Declarative Language Model Calls into Self-Improving Pipelines

## Citation

Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T.T., Moazam, H., Miller, H., Zaharia, M., & Potts, C. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." ICLR 2024. arXiv:2310.03714.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_khattab2023dspy_intro](paper_khattab2023dspy_intro.md) | Prompt engineering is brittle; need for declarative LM programming |
| **Contributions** | [paper_khattab2023dspy_contrib](paper_khattab2023dspy_contrib.md) | Signatures, modules, teleprompters; interface/implementation separation |
| **Algorithm** | [paper_khattab2023dspy_algo](paper_khattab2023dspy_algo.md) | Compilation process, optimizer types, composable module architecture |
| **Experiment Design** | [paper_khattab2023dspy_exp_design](paper_khattab2023dspy_exp_design.md) | GSM8K, HotPotQA benchmarks; comparison with hand-crafted prompts |
| **Experiment Results** | [paper_khattab2023dspy_exp_result](paper_khattab2023dspy_exp_result.md) | +25-65% over few-shot; small models compete with GPT-3.5 expert chains |
| **Review** | [review_khattab2023dspy](review_khattab2023dspy.md) | OpenReview-style; 4 strengths, 4 weaknesses, 5 questions; Soundness 3/4, Overall 8/10 |

## Core Idea

**DSPy** introduces a **declarative programming model** for LLM pipelines where developers specify *what* each module should do (via **signatures** — input/output declarations) while **optimizers** (teleprompters) automatically determine *how* — by bootstrapping demonstrations, proposing instructions, and searching over configurations. This decouples the **interface** (task specification) from the **implementation** (prompt engineering), making LLM pipelines composable, portable across models, and self-improving.

The key insight: **prompt engineering should be compiled, not hand-crafted.** Just as high-level programming languages compile to machine code, DSPy compiles declarative module specifications into optimized prompts or fine-tuned weights.

## Key Takeaways

1. **Signatures as atomic interfaces**: A signature like `"question -> answer"` or `"context, question -> rationale, answer"` defines the module's contract — what goes in, what comes out. This is the **atomic unit** of an LLM pipeline.
2. **Modules as composable building blocks**: Built-in modules (Predict, ChainOfThought, ReAct, ProgramOfThought) can be nested and composed into complex pipelines — each module is independently optimizable.
3. **Teleprompters/Optimizers replace prompt engineering**: BootstrapFewShot, MIPRO, GEPA automatically discover effective prompts/demonstrations — no manual prompt tuning.
4. **Compilation = automated optimization**: `dspy.compile()` takes a program + training examples + metric → produces an optimized pipeline. This is analogous to compiling source code.
5. **Small models can compete with large**: T5-770M and llama2-13b with DSPy optimization achieve performance competitive with GPT-3.5 expert-crafted chains.

## Relevance to Abuse Slipbox

DSPy's architecture directly parallels the Abuse SlipBox's skill system:

| DSPy Concept | SlipBox Equivalent |
|-------------|-------------------|
| **Signature** | Skill's `argument-hint` + expected output format |
| **Module** | Individual skill (e.g., `/slipbox-capture-term-note`) |
| **Composed pipeline** | Skill chain (search → save → digest → review → capture term) |
| **Teleprompter** | Meta-Harness-style optimization of skill code |
| **Compilation** | Not yet implemented — but the SlipBox's skill pipelines could be "compiled" |

**Key difference**: DSPy optimizes *prompts and demonstrations*; the SlipBox's skills optimize the *entire harness* (retrieval strategy, context assembly, output formatting). Meta-Harness (Lee et al., 2026) addresses this gap — it optimizes harness code, not just prompts.

**Key connection**: DSPy's Omar Khattab is also a co-author of Meta-Harness — the two systems form a progression: DSPy optimizes prompt-level modules; Meta-Harness optimizes code-level harnesses.

## Related Notes

- [Meta-Harness Literature Note](lit_lee2026metaharness.md) — Co-authored by Khattab; extends DSPy's optimization to full harness code
- [Meta-Harness Lens Analysis](../analysis_thoughts/analysis_metaharness_lens_on_abuse_slipbox.md) — Skills as harnesses
- [Agentic Pipeline Analysis](../analysis_thoughts/analysis_agentic_pipelines_skill_chaining.md) — 15 skill pipelines as composed modules
- [Term: Meta-Harness](../term_dictionary/term_meta_harness.md) — Harness optimization beyond DSPy
- [Term: LLM](../term_dictionary/term_llm.md) — The models DSPy programs

---

**Last Updated**: 2026-04-10
