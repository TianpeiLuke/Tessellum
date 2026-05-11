---
tags:
  - resource
  - papers
  - literature_note
  - llm
  - tool_use
  - agentic_ai
  - cost_optimization
keywords:
  - LATM
  - LLM as Tool Maker
  - tool creation
  - tool use
  - functional caching
  - amortized cost
  - two-phase framework
  - GPT-4
  - GPT-3.5
  - tool dispatch
topics:
  - LLM Systems
  - Tool Use
  - Cost Optimization
  - Agentic AI
language: markdown
date of note: 2026-04-10
status: active
building_block: hypothesis
paper_id: cai2023latm
arxiv_id: "2305.17126"
doi: "10.48550/arXiv.2305.17126"
citation_count: 276
year: 2023
venue: ICLR 2024
paper_notes:
  - paper_cai2023latm_intro.md
  - paper_cai2023latm_contrib.md
  - paper_cai2023latm_algo.md
  - paper_cai2023latm_exp_design.md
  - paper_cai2023latm_exp_result.md
---

# Literature Note: Large Language Models as Tool Makers (LATM)

## Citation

Cai, T., Wang, X., Ma, T., Chen, X., & Zhou, D. (2023). "Large Language Models as Tool Makers." ICLR 2024. arXiv:2305.17126.

## Table of Contents

| Section | Note | Key Content |
|---------|------|-------------|
| **Introduction** | [paper_cai2023latm_intro](paper_cai2023latm_intro.md) | LLM inference cost problem; tool use vs tool creation |
| **Contributions** | [paper_cai2023latm_contrib](paper_cai2023latm_contrib.md) | Two-phase framework, functional caching, tool dispatch |
| **Algorithm** | [paper_cai2023latm_algo](paper_cai2023latm_algo.md) | Tool making process, dispatch logic, architecture diagram |
| **Experiment Design** | [paper_cai2023latm_exp_design](paper_cai2023latm_exp_design.md) | Big-Bench Hard; GPT-4 maker + GPT-3.5 user |
| **Experiment Results** | [paper_cai2023latm_exp_result](paper_cai2023latm_exp_result.md) | Performance parity with GPT-4-only at lower cost |
| **Review** | [review_cai2023latm](review_cai2023latm.md) | 4 strengths, 3 weaknesses; Soundness 3/4, Overall 7/10 |

## Core Idea

**LATM** introduces a two-phase framework separating **tool creation** (by a powerful LLM like GPT-4) from **tool use** (by a lightweight LLM like GPT-3.5). The powerful model generates reusable Python functions for classes of problems; the lightweight model applies cached tools to solve new instances. This achieves performance parity with using GPT-4 for everything but at significantly lower cost — the tool-making expense is amortized across many tool-using instances.

The key insight: **functional caching** — instead of caching responses (which are instance-specific), cache the *function* that generates responses (which is class-general). A cached tool is reusable across all instances of a problem class.

## Key Takeaways

1. **Separate creation from use**: Tool making is expensive but one-time; tool use is cheap and repeated. The economic analogy: invest in building a factory (tool) to mass-produce outputs (answers).
2. **Functional caching > response caching**: A cached Python function generalizes to new inputs; a cached response is useless for different inputs.
3. **Model role specialization**: GPT-4 as the "tool maker" (creative, expensive); GPT-3.5 as the "tool user" (efficient, cheap). Different models for different cognitive demands.
4. **Tool dispatch**: A dispatcher routes incoming problems to existing cached tools or triggers tool creation for new problem classes.

## Relevance to Abuse Slipbox

LATM's framework is a **direct analogy** to the Abuse SlipBox's skill architecture:

| LATM | Abuse SlipBox |
|------|---------------|
| **Tool Maker** (GPT-4) | Human skill designer (writes SKILL.md) |
| **Tool User** (GPT-3.5) | Agent executing the skill |
| **Tool** (Python function) | Skill (structured workflow in SKILL.md) |
| **Tool Cache** | `.claude/skills/` directory |
| **Tool Dispatch** | Claude Code skill matching from description |
| **Functional caching** | Skill reuse across invocations |

The human invests time designing a skill (expensive, one-time) so the agent can execute it repeatedly (cheap, many times). **The SlipBox's 60+ skills are LATM's tool cache** — each skill is a "functional cache" encoding a reusable knowledge workflow.

**Key difference**: LATM's tools are simple Python functions; the SlipBox's skills are full harnesses (retrieval + context assembly + output formatting + database updates). Meta-Harness bridges this gap — optimizing the harness, not just the function.

## Related Notes

- [DSPy Literature Note](lit_khattab2023dspy.md) — Composable modules; DSPy's signatures parallel LATM's tool interfaces
- [Meta-Harness Literature Note](lit_lee2026metaharness.md) — Extends LATM from tool-level to harness-level optimization
- [Term: LATM](../term_dictionary/term_latm.md) — Term definition
- [Term: DSPy](../term_dictionary/term_dspy.md) — Declarative module compilation
- [Term: Meta-Harness](../term_dictionary/term_meta_harness.md) — Harness optimization
- [Term: Toolformer](../term_dictionary/term_toolformer.md) — Tool use (not creation)
- [Term: Voyager](../term_dictionary/term_voyager.md) — Skill library for embodied agents
- [Agentic Pipeline Analysis](../analysis_thoughts/analysis_agentic_pipelines_skill_chaining.md) — SlipBox's skill pipelines as LATM's tool chains

---

**Last Updated**: 2026-04-10
