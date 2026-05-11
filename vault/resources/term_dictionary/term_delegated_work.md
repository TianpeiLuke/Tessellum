---
tags:
  - resource
  - terminology
  - llm_evaluation
  - agentic_ai
  - human_ai_interaction
  - knowledge_work
keywords:
  - delegated work
  - vibe coding
  - knowledge work delegation
  - LLM faithful execution
  - long-horizon delegation
  - AI delegate
  - delegated workflow
  - supervised handoff
topics:
  - AI Interaction Paradigms
  - Knowledge Work
  - LLM Reliability
language: markdown
date of note: 2026-04-28
status: active
building_block: concept
related_wiki: null
---

# Delegated Work — Knowledge-Work Handoff to LLMs

## Definition

**Delegated Work** is an emerging LLM interaction paradigm in which knowledge workers hand off complete tasks to an LLM and supervise (rather than author) the resulting changes. The user retains the *expertise* to review the output but no longer has the *time* (or no longer needs) to perform the task themselves. The canonical example is "vibe coding", where a developer describes desired changes at a high level and trusts the LLM to implement them faithfully across a codebase. In contrast to chat-style co-authoring or interactive editing, delegation hinges on *trust* — the expectation that the LLM will execute the task without introducing unchecked errors (hallucinations, deletions, silent corruption) into the artifact being worked on.

The viability of delegated work hinges on two LLM properties: (i) cross-domain faithfulness across the diversity of professional knowledge work, and (ii) long-horizon reliability across multi-turn workflows where errors compound. The DELEGATE-52 benchmark (Laban et al., 2026) operationalizes both properties for empirical study.

## Context

Delegated work as a research framing emerged in 2025-2026 alongside agentic AI tooling:

- **Vibe coding** (popularized 2024-2025) — high-level natural-language coding requests where developers supervise rather than author each change. Tools: Cursor Composer, Claude Code, Replit Agent, Bolt.
- **Knowledge worker integration of LLMs** — Bick et al. (2024) report ~40% of working-age Americans used generative AI at work in late 2024; Brachman et al. (2024) survey active LLM integration into workflows.
- **Beyond chat** — delegated work is positioned as the paradigm *after* chat (single-turn) and *after* basic agent-with-tools. The user moves further from the artifact, supervising outcomes rather than steps.

Within Amazon buyer-abuse prevention, delegated-work concerns map onto:

- LLM-driven **investigator pipelines** (e.g., [Greentea LLM Pipeline](../../areas/models/model_greentea_llm_pipeline.md), [SOPA LLM Pipeline](../../areas/models/model_sopa_llm_pipeline.md)) — the LLM produces case decisions and policy citations the human then reviews; trust in faithful execution is critical.
- **Automated case enforcement** — when a model's output is the action (refund, decision, restoration), the operator delegates the artifact creation to the model.
- **Multi-step LLM workflows** — pipelines that ingest evidence, summarize, classify, and explain are subject to the same long-horizon degradation patterns DELEGATE-52 studies.

## Key Characteristics

- **Outcome-supervised, not step-supervised**: the user reviews the final artifact, not each intermediate edit.
- **Trust-bounded**: the value of delegation is bounded by the user's trust in faithful execution; trust collapses if silent errors are detected.
- **Long-horizon**: a delegated task may span many turns or many edits; errors compound across iterations.
- **Cross-domain**: real knowledge work spans many professional domains, not just code, so "domain readiness" varies.
- **Reference-free supervision**: the user supervises by inspection, not by comparison to a known-good answer; this requires the user retains domain expertise.
- **Failure mode is *silent corruption***: the most dangerous failures are not refusals or visible hallucinations but small-but-severe errors introduced quietly into the artifact.
- **Asymmetric cost**: a single critical failure (Laban et al. 2026 define this as a ≥10pt single-step quality drop) can require recreating the artifact from scratch, while small errors are tolerable.

## Performance / Metrics

From DELEGATE-52 (Laban et al., 2026), 19 LLMs evaluated on 310 work environments across 52 domains:

- Frontier models (Gemini 3.1 Pro, Claude 4.6 Opus, GPT 5.4) corrupt ~25% of document content over 20 interactions.
- Average across all 19 models: ~50% degradation by interaction 20.
- Python is the only domain where a majority of tested models (17/19) achieve ≥98% reconstruction (the "ready" threshold).
- The top model (Gemini 3.1 Pro) is "ready" in only 11/52 domains.
- Tool use (basic agentic harness): degrades performance by an additional ~6%, with 2-5× input-token overhead.
- Critical failures (≥10pt single-round drops) account for ~80% of total document degradation.

## Related Terms

- **[Agentic AI](term_agentic_ai.md)**: delegated work is the next interaction paradigm beyond agent-with-tools; agentic AI provides the substrate (tools, memory, planning) but delegation reframes the user's role from operator to supervisor.
- **[Agentic Evaluation](term_agentic_evaluation.md)**: delegated work demands long-horizon, cross-domain agentic evaluation; the DELEGATE-52 benchmark is one such instance.
- **[Agentic Memory](term_agentic_memory.md)**: long-horizon delegation interacts with memory — single-turn evaluations like DELEGATE-52 deliberately exclude memory to isolate per-step faithfulness.
- **[Hallucination](term_hallucination.md)**: silent-corruption failures in delegated work are an extension of hallucination — sparse, severe, embedded in otherwise correct output.
- **[Round-Trip Relay](term_round_trip_relay.md)**: methodological primitive for evaluating LLM faithfulness in delegated workflows without reference solutions.
- **[Critical Failure (LLM)](term_critical_failure.md)**: dominant failure mode in delegated work — single-step large-magnitude drops that account for most cumulative degradation.
- **[Evaluation Harness](term_evaluation_harness.md)**: frameworks for measuring LLM performance; delegated-work evaluation requires harnesses that simulate long workflows, not single-turn benchmarks.
- **[MT-Bench](term_mt_bench.md)**: contrasts methodologically — MT-Bench uses LLM-as-judge for chat; delegated-work eval (DELEGATE-52) uses domain-specific parsers for objective scoring.
- **[Self-Evolving Agent](term_self_evolving_agent.md)**: a related research direction; agents that improve through interaction must avoid corrupting the artifacts they evolve over.
- **[RAG](term_rag.md)**: distractor-context findings in delegated work evaluation directly inform retrieval system design — long-horizon benchmarks capture lasting effects of imperfect retrieval.
- **[LLM](term_llm.md)**: the substrate; delegation is one mode of LLM use, alongside chat, classification, and retrieval-augmented generation.
- **[Greentea](term_greentea.md)**: BRP investigation system; delegated-work findings on long-horizon degradation are directly applicable to multi-turn LLM-based investigator pipelines.
- **[Knowledge Graph](term_knowledge_graph.md)**: related infrastructure — supervisable artifacts include KGs, where edits must preserve graph semantics rather than corrupt nodes/edges.

## References

- [LLMs Corrupt Your Documents When You Delegate (Laban et al., 2026)](../papers/lit_laban2026llms.md) — the canonical study introducing DELEGATE-52 and the long-horizon delegation framing
- [arXiv:2604.15597](https://arxiv.org/abs/2604.15597) — full paper
- [DELEGATE-52 GitHub](https://github.com/microsoft/DELEGATE52) — code and benchmark release
- [DELEGATE-52 Dataset](https://huggingface.co/datasets/microsoft/DELEGATE52) — work environments and tasks
