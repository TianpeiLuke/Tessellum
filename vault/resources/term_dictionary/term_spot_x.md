---
tags:
  - resource
  - terminology
  - buyer_abuse_prevention
  - machine_learning
  - llm
  - prompt_optimization
  - rule_generation
keywords:
  - SPOT-X
  - Structured Prompt Optimization for Text Classification with Explanations
  - prompt optimization
  - rule generation
  - rule mining
  - abuse detection rules
  - decision set
  - interpretable rules
  - SOP disambiguation
  - textual gradients
topics:
  - LLM prompt optimization
  - abuse rule generation
  - SOP alignment
  - rule mining
  - buyer abuse prevention automation
language: markdown
date of note: 2026-03-02
status: active
building_block: concept
related_wiki: https://quip-amazon.com/grQbA0joEY3E/PRFAQ-SPOT-X-for-Abuse-Rule-Generation-Mining-and-Detection
---

# SPOT-X - Structured Prompt Optimization for Text Classification with Explanations

## Definition

SPOT-X is an AI-powered system developed by the MLA (Machine Learning Analytics) team that automatically generates **disambiguated, interpretable abuse detection rules** from production data. Unlike traditional prompt optimization tools (TextGrad, ProTeGi, GreenTEA) which produce a single lengthy and often ambiguous prompt, SPOT-X outputs a **structured decision set** — a collection of natural-language rules each with explicit conditions, exceptions, and chain-of-thought example cases that can be reviewed in under 5 minutes per rule.

The system operates through "verbalized" ML: it uses LLMs to derive "textual gradients" for rule updates and candidate generation, then applies principled subset optimization to select a succinct decision set with minimal classification error. The composability of its decision sets — where final decisions pool across individual rule predictions — enables efficient combinatorial search while requiring only linear (not exponential) LLM calls in the number of rules.

## Context

SPOT-X addresses a critical alignment gap in Amazon's buyer abuse prevention program: ARI (Abuse Risk Investigator) and TPM teams historically achieved only 20% agreement in abuse detection decisions, and RnR (Reversal and Reclassification) investigations uncovered ~$112 million in false-positive monetary impact in 2024. SPOT-X was developed to resolve ambiguous SOPs at the source by automatically mining and generating structured, auditable rules that bridge ML scientists, TPMs, and investigators.

SPOT-X is used by the MLA team and integrates with:
- **Abuse Slipbox** — provides unified context for prompt generation
- **Tattletale-Nexus** — MO behavior summarization and action mapping
- **Paragon BSM Summarizer** — guided workflow for ARI with action suggestions
- **RnR automation pipeline** — continuous improvement for live LLM inference
- **Post Investigation Workflow (PIW)** — audits ARI decisions to reduce label noise
- **CS-MO Detection** — discovers MO patterns from CS chat reviews
- **Returnless Refund definition alignment** — aligns PM and ML on RR detection

## Key Characteristics

- **Decision set output**: Rules are stand-alone natural-language statements that make independent predictions; composability means any subset of rules can be evaluated without re-running the full model
- **Textual gradient optimization**: LLMs generate candidate rules and evaluate their contribution to classification error — the system searches a combinatorial rule space with only O(n) LLM calls
- **Three core capabilities**:
  1. **Knowledge Extraction & Summarization** — integrates with Slipbox context engine and Nexus KG for MO behavior summarization
  2. **Rule Generation & Optimization** — automated pipeline for RnR, PIW, and BSM Summarizer integration
  3. **Rule Mining** — discovers patterns from CS chat (CS-MO), Returnless Refund abuse, and ambiguous SOPs
- **Human-auditable in <5 minutes per rule** — structured conditions/exceptions/examples format designed for rapid TPM and senior ARI review
- **SOP-native output** — rules are directly integrable into SOPs without manual translation, unlike prompt-only systems
- **General-purpose framework** — while designed for buyer abuse detection (PDA, DNR, RR), the framework applies to any text classification task

## Performance / Metrics

| Task | Metric | Before SPOT-X | After SPOT-X | Improvement |
|------|--------|---------------|--------------|-------------|
| PDA Detection | F1 Score | 0.49 | 0.65 | +32.7% |
| PDA Detection | Accuracy | 75% | 89% | +14 pp |
| DNR Detection | F1 Score | 0.74 | 0.86 | +16.2% |
| DNR Detection | Accuracy | 73% | 82% | +9 pp |
| Rule Review Time | — | Weeks | <5 min/rule | ~75% reduction |
| ARI/TPM Alignment | Agreement | 20% | Significant improvement | Disambiguation success |

Business context: $112M in 2024 RnR false-positive monetary impact that SPOT-X targets through SOP disambiguation and alignment.

## Related Terms

- **[GreenTEA](term_greentea.md)**: Closest sibling — also LLM-based prompt optimization for abuse decisions, but produces a single optimized prompt rather than structured decision rules; SPOT-X is explicitly designed to improve interpretability beyond GreenTEA
- **[SOPA](term_sopa.md)**: SOP-aware LLM for BRW automation; SPOT-X generates the structured rules that SOP-aware systems like SOPA follow
- **[SOP](term_sop.md)**: Standard Operating Procedure; SPOT-X's primary output is rule sets that directly augment and disambiguate SOPs
- **[LLM](term_llm.md)**: SPOT-X is powered by LLMs for textual gradient generation and candidate rule evaluation
- **[RnR](term_rnr.md)**: Reversal and Reclassification program is a primary SPOT-X integration target for continuous improvement of live LLM inference
- **[RMP](term_rmp.md)**: Rule Management Platform; SPOT-X-generated rules may feed into RMP for rule lifecycle management
- **[ARROW Everywhere](term_arrow_everywhere.md)**: Rule optimization system; SPOT-X complements it by generating new rules from data rather than optimizing existing rule thresholds
- **[Prompt Optimization](term_prompt_optimization.md)**: SPOT-X uses TextGrad-style textual gradient descent for structured prompt optimization; ACE framework extends this with incremental delta updates and evolving playbooks

## References

- [PRFAQ: SPOT-X for Abuse Rule Generation, Mining and Detection](https://quip-amazon.com/grQbA0joEY3E/PRFAQ-SPOT-X-for-Abuse-Rule-Generation-Mining-and-Detection)
- [SPOT-X Experiment for PDA & DNR Detection](https://quip-amazon.com/PnShA0ir7ozN)
- [SPOT-X Paper (WorkDocs)](https://amazon.awsapps.com/workdocs-amazon/index.html#/document/614068eaca32ba4c64b3cce3ddc328fa86207e51ccb6047b6e3194da1ed7ebba)
- [CS-MO Detection Launch](https://quip-amazon.com/xsG0AwIirkcp)
- [Returnless Refund Definition Alignment](https://quip-amazon.com/iRkZA9mDEnR2)
- [Reversal and Reclassification Program Overview](https://quip-amazon.com/EPteAk1T1qjx)
- [Post Investigation Workflow](https://quip-amazon.com/7nnGApIk1wn0)
- [Internal PRFAQ notes](../documentation/prfaq/prfaq_spot_x.md)


## Code Repositories
- [Project: SPOT-X](../../projects/project_spot_x.md)

- [Repo: SpotX](../../areas/code_repos/repo_spotx.md) — Core optimization framework (runner, rule models, beam search, LiteLLM engines)
- [Repo: SpotXLambdas](../../areas/code_repos/repo_spotx_lambdas.md) — Lambda API service (execution management, S3 presigned URLs, Step Functions)

---

**Last Updated**: 2026-04-11
