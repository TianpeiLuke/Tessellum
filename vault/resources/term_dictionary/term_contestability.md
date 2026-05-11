---
tags:
  - resource
  - terminology
  - argumentation
  - explainable_ai
  - ai_governance
  - human_ai_interaction
  - critical_thinking
keywords:
  - contestability
  - contestable AI
  - base score contestability
  - argument relation contestability
  - explainability vs contestability
  - faithful explanation
  - QBAF
  - DF-QuAD
  - Leofante
  - Toni
  - human oversight
topics:
  - Explainable AI
  - AI Governance
  - Computational Argumentation
language: markdown
date of note: 2026-04-25
status: active
building_block: concept
related_wiki: null
---

# Contestability

## Definition

**Contestability** is the formal property of an AI system whereby an external agent — typically a human user, but possibly another AI agent — can **disagree with**, **intervene on**, and **demonstrably alter** the system's automated decisions through targeted, well-defined modifications to its internal reasoning artefacts. Unlike *explainability* (which is *descriptive* — the system reveals how it reached a decision) or *interpretability* (which is *structural* — the system's representations are human-readable), contestability is *interactive*: it requires the system to expose handles that, when pulled, produce a measurable, traceable change in the output. It is studied as a property both for AI systems in general (Henin & Métayer 2022; Lyons et al. 2021; Leofante, Ayoobi, Dejl & Toni 2024) and for argumentation-based AI in particular (Cyras et al. 2021).

In the context of ArgLLMs (Freedman et al. 2025), contestability is *operationalised* as two formal properties of a gradual semantics $\sigma$ over a [QBAF](term_qbaf.md). **Base Score Contestability** (Property 1) requires that, holding the argument and relation sets fixed, decreasing the base score $\tau(\beta)$ of any *pro* argument $\beta \in \text{pro}(Q)$ (and increasing it for any *con* argument) cannot increase the strength of the target argument $\alpha^*$ — and vice versa. **Argument Relation Contestability** (Property 2) requires that adding a new attacker $\delta$ to a pro argument (or to an even-length attack chain leading to $\alpha^*$) cannot increase $\sigma(\alpha^*)$, and an analogous monotonicity for new supporters and new attackers on con arguments. Freedman et al. prove that the [DF-QuAD](term_df_quad.md) gradual semantics satisfies both properties, which is what allows their ArgLLM pipeline to claim provable contestability guarantees.

## Context

Contestability has emerged as a first-class desideratum for high-stakes AI deployment in legal, medical, financial, and content-moderation settings, where regulators and affected parties demand more than a post-hoc rationalisation: they demand the **right to push back**. The concept appears across at least four research programmes: (i) **HCI and AI ethics** — Lyons et al. (2021), Henin & Métayer (2022), and Mulligan et al. on contestable design — frame contestability as a procedural and interface requirement; (ii) **EU AI Act and "right to challenge automated decisions"** literature, where contestability is the engineering correlate of GDPR Article 22; (iii) **argumentation-based AI** — Cyras et al. (2021) and Leofante et al. (2024) treat contestability as a structural property of the reasoning representation; and (iv) **LLM safety and oversight** — recent work (Freedman et al. 2025; Rago et al. 2024) frames contestability as the missing piece in LLM "explanations" that are otherwise post-hoc and unfaithful (Turpin et al. 2023).g., lowering a stale-case-history feature's weight) and watching the verdict flip is *contestable*; one that requires a re-run with hidden internals is not.

## Key Characteristics

- **Interactive, not merely descriptive**: contestability requires that the system *change* in response to a user intervention; merely *displaying* its reasoning is explainability, not contestability.
- **Requires editable handles**: the system must expose well-defined points of intervention — base scores, argument inclusion / exclusion, edge labels — that the user can modify.
- **Requires measurable downstream effect**: edits must propagate deterministically through the reasoning pipeline so the user can verify that the edit caused the verdict change.
- **Two formalised flavours in ArgLLMs (Freedman et al. 2025)**:
  - **Base Score Contestability** — monotonic dependence of $\sigma(\alpha^*)$ on $\tau(\beta)$ of any pro / con argument, holding the graph fixed.
  - **Argument Relation Contestability** — monotonic dependence of $\sigma(\alpha^*)$ on the addition / removal of attackers and supporters in the argument graph.
- **Provable for DF-QuAD**: Freedman et al. (2025) prove DF-QuAD satisfies both properties; stronger strict-inequality variants are satisfied by the Quadratic Energy semantics (Potyka 2018).
- **Distinct from explainability**: a system can be explainable without being contestable (e.g., a fixed saliency map) and contestable without being fully explainable (the user can poke and observe even without understanding internals).
- **Stronger than transparency**: transparency reveals the *what*; contestability guarantees the *what changes when I push back*.
- **Necessary for human oversight at scale**: in pipelines that emit thousands of decisions per second, contestability is the engineering mechanism that lets a small expert team intervene on the few cases that matter (appeals, audits, edge cases).
- **Compatible with — but not subsumed by — counterfactual explanations**: counterfactuals describe *what would have made the decision different*; contestability lets the user *actually do it* and verify the system honours it.
- **Bounded by the editable surface**: a system is only contestable up to the level of granularity its handles expose; an LLM whose only handle is the prompt is contestable only at the prompt level.

## Related Terms

- **[QBAF](term_qbaf.md)**: the structured representation that gives ArgLLMs their editable handles — base scores and attack / support edges — making contestability formally definable
- **[DF-QuAD](term_df_quad.md)**: the gradual semantics proven to satisfy both Base Score and Argument Relation Contestability over QBAFs
- **[Argumentation](term_argumentation.md)**: the parent field that has long treated arguments as objects to be challenged; contestability is the algorithmic refinement of this norm for AI systems
- **[Dialectic Knowledge System](term_dialectic_knowledge_system.md)**: a vault knowledge architecture where contestability is a built-in property — every claim is paired with explicit, editable warrants and counter-arguments
- **[Dialectical Adequacy](term_dialectical_adequacy.md)**: a dialectically adequate argument is one that has survived contestation; contestability is the *interface* by which adequacy is tested
- **Hallucination**: contestability is one of the most promising mitigations for LLM hallucinations — a hallucinated reason becomes a contestable argument that a human reviewer can suppress
- **Chain of Thought**: CoT explanations are not contestable in any formal sense — re-prompting may or may not change the answer in a traceable way; contestability is what CoT lacks
- **LLM as a Judge**: an LLM-as-judge verdict is contestable only if the rubric scores it produces are themselves editable by a human reviewer with deterministic downstream effect
- **Multi-Agent Debate**: MAD provides multiple perspectives but does not by itself give the user editable handles into the resolution process; contestability is the additional structural property that QBAF-based aggregation supplies
- **Counterfactual Reasoning**: contestability is the operational realisation of counterfactual reasoning — "what would have changed the decision?" becomes a button the user can press
- **Logical Fallacies**: a contestable system lets a user mark a fallacious argument as low-strength and watch the verdict update — a powerful tool for collaborative reasoning hygiene
- **[Critical Thinking](term_critical_thinking.md)**: contestability is the AI-system-design analogue of the critical-thinking habit of treating every conclusion as provisional and revisable in light of stronger reasons
- **Neuro-Symbolic**: contestability is most easily achieved by neuro-symbolic systems where the symbolic component is the deterministic, editable substrate — as in ArgLLMs (LLM + QBAF + DF-QuAD)
- **Steelmanning**: a contestable system invites steelmanning — users can add the strongest possible attacker to the QBAF and observe whether the verdict actually changes
- **Active Listening**: the user-side complement to contestability — to contest well, the user must first carefully read the system's argument graph rather than reacting to its bottom line
- **Hallucination**: contestability mitigates downstream harm from hallucinated reasoning by exposing each hallucinated artefact as an editable, weight-adjustable node

## References

- [Freedman, Dejl, Gorur, Yin, Rago & Toni (2025). "Argumentative Large Language Models for Explainable and Contestable Claim Verification." AAAI 2025 (oral)](https://arxiv.org/abs/2405.02079) — defines and formally proves Base Score Contestability and Argument Relation Contestability for DF-QuAD over QBAFs
- [Leofante, Ayoobi, Dejl & Toni (2024). "Contestable AI Needs Computational Argumentation." KR 2024](https://arxiv.org/abs/2405.10729) — argues that computational argumentation is the natural substrate for contestable AI
- [Henin & Le Métayer (2022). "Beyond Explainability: Justifiability and Contestability of Algorithmic Decision Systems." AI & Society](https://link.springer.com/article/10.1007/s00146-021-01251-8) — distinguishes explainability, justifiability, and contestability as separate AI-governance requirements
- [Lyons, Velloso & Miller (2021). "Conceptualising Contestability: Perspectives on Contesting Algorithmic Decisions." CHI 2021](https://dl.acm.org/doi/10.1145/3449180) — HCI framing of contestability as a design requirement for algorithmic decision systems
- [Mulligan, Kluttz & Kohli (2019). "Shaping Our Tools: Contestability as a Means to Promote Responsible Algorithmic Decision Making." Available at SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3311894) — early articulation of contestability as a normative requirement for responsible AI
- [Cyras, Rago, Albini, Baroni & Toni (2021). "Argumentative XAI: A Survey." IJCAI](https://www.ijcai.org/proceedings/2021/0600.pdf) — survey of argumentation-based XAI, including contestability as a desideratum
- [Rudin (2019). "Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead." Nature Machine Intelligence](https://www.nature.com/articles/s42256-019-0048-x) — the classic case for intrinsically interpretable models, a precondition for meaningful contestability
- [Turpin, Michael, Perez & Bowman (2023). "Language Models Don't Always Say What They Think." NeurIPS](https://arxiv.org/abs/2305.04388) — empirical demonstration that CoT reasoning is often unfaithful, motivating the need for contestable, deterministic alternatives
- [Wikipedia. "Right to explanation."](https://en.wikipedia.org/wiki/Right_to_explanation) — overview of the regulatory backdrop (GDPR Article 22) that motivates contestability research
