---
tags:
  - resource
  - terminology
  - knowledge_management
  - zettelkasten
  - procedural_knowledge
keywords:
  - procedure
  - procedural knowledge
  - knowing-how
  - workflow
  - runbook
  - standard operating procedure
  - step-by-step
  - knowledge building block
  - vault extension
topics:
  - Knowledge Management
  - Zettelkasten Method
  - Procedural Knowledge
  - Operations
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
author: lukexie
---

# Term: Knowledge Building Blocks -- Procedure

## Definition

A **Procedure** is a knowledge building block that encodes step-by-step action sequences for execution. Procedure notes answer the question "how do I do X?" with an ordered sequence of concrete actions. Unlike argument notes (which reason toward a conclusion) or observation notes (which record what was seen), procedure notes prescribe what to do and in what order. They are the operational backbone of a knowledge system -- the notes that team members reach for when they need to investigate a case, run a pipeline, or execute a workflow.

**Vault Extension**: Procedure is not part of Sascha Fast's original six knowledge building blocks (premises, logical form, conclusions, definitions, distinctions, heuristics) nor his expanded taxonomy (concepts, arguments, hypotheses, empirical observations). It was added to this vault's taxonomy because operational knowledge systems -- particularly those supporting abuse investigation, ML model operations, and incident response -- require explicit procedural knowledge as a first-class note type. The philosophical grounding comes from Gilbert Ryle's distinction between "knowing-that" (propositional knowledge, which Sascha's blocks capture well) and "knowing-how" (procedural knowledge, which requires its own building block). A procedure note does not argue that something is true; it instructs how something is done. This distinction matters because procedural notes have different quality criteria (completeness of steps, ordering correctness, prerequisite clarity) than argumentative notes (logical validity, evidential support).

## Historical Origin

The recognition that procedural knowledge is categorically different from propositional knowledge has a rich philosophical and cognitive science lineage:

| Contributor | Work | Key Contribution |
|-------------|------|-------------------|
| **Gilbert Ryle** | *The Concept of Mind* (1949) | Distinguished **knowing-how** from **knowing-that**. Argued that practical skills and procedural competence cannot be reduced to propositional statements. A chef's ability to make a sauce is not equivalent to knowing the recipe's facts. |
| **John Anderson** | ACT* Theory (1983) | Proposed the **ACT* cognitive architecture** distinguishing declarative memory (facts) from procedural memory (production rules). Procedural learning involves compiling declarative knowledge into automated action sequences through practice. |
| **Sascha Fast's framework, extended by vault practice** | Zettelkasten.de (2025) + vault convention | Sascha's taxonomy covers propositional building blocks comprehensively. The vault's operational needs -- SOPs, runbooks, investigation procedures -- demanded a dedicated procedural block type. This extension follows Ryle's logic: if knowing-how is irreducible to knowing-that, the building block taxonomy needs a procedural type. |

The vault extension is principled, not ad hoc. Ryle's argument that procedural knowledge is categorically distinct from propositional knowledge provides the philosophical justification. Anderson's ACT* theory provides the cognitive science evidence. The vault's operational experience provides the practical necessity.

## Recognition Criteria

Your note is a procedure building block if it:

- Contains **numbered steps** -- an ordered sequence of actions that must be performed in a specific order
- Describes a **workflow** -- a multi-step process with decision points, branching paths, or handoff points between actors
- Functions as a **runbook** -- a document that guides an operator through a specific operational task (investigation, deployment, incident response)
- Provides **how-to instructions** -- explicit guidance on performing a task, using a tool, or executing a process
- Specifies **prerequisites** -- what must be true, available, or completed before the procedure can begin
- Includes **expected outcomes** -- what the operator should see or have produced after completing each step or the procedure as a whole
- Can be summarized as "to accomplish X, do steps 1, 2, 3..." rather than "X is true because..." or "we observed X"

A useful formalization: a procedure $P$ is a sequence of actions $(a_1, a_2, \ldots, a_n)$ where each action $a_i$ has preconditions $\text{pre}(a_i)$ and postconditions $\text{post}(a_i)$, and $\text{pre}(a_{i+1}) \subseteq \text{post}(a_i)$ for sequential steps.

## Writing Guide

A good procedure note should:

- **Start with purpose and scope** -- one sentence stating what the procedure accomplishes and when to use it
- **List prerequisites explicitly** -- tools required, permissions needed, prior steps completed, data available. Never assume the reader knows the setup
- **Number all steps sequentially** -- use ordered lists, not bullet points. Order matters in procedures; bullet points imply unordered items
- **Make each step a single action** -- "Open the dashboard and check the metric and export the report" is three steps, not one
- **Include verification checkpoints** -- after critical steps, tell the operator what they should see to confirm the step succeeded
- **Link to conceptual background, do not embed it** -- if a step requires understanding a concept (e.g., what a false positive rate means), link to the term note rather than explaining it inline. Procedures should be lean and scannable
- **Specify error handling** -- what should the operator do if a step fails? Who should they escalate to? What is the rollback procedure?

## Vault Examples

| Example Note | Why It Is a Procedure |
|--------------|------------------------|
| ARI SOP notes (e.g., [ari_sop_reseller_writebacks_overview.md](../policy_sops/ari_sop_reseller_writebacks_overview.md)) | Standard operating procedures for abuse investigators: step-by-step guides for reviewing cases, applying enforcement actions, and documenting decisions. Canonical procedure notes. |
| How-to guides in [entry_how_to_guides.md](../../0_entry_points/entry_how_to_guides.md) | Guides that walk operators through specific tasks: how to set up a development environment, how to run an ETL job, how to deploy a model. Pure procedural content. |
| Role guidelines in [entry_role_guidelines.md](../../0_entry_points/entry_role_guidelines.md) | Documents describing what actions a person in a specific role should perform, in what order, and under what conditions -- procedural knowledge scoped to organizational roles. |

## Common Mistakes

- **Mixing conceptual background into procedures**: Embedding three paragraphs explaining *why* a step matters before stating *what* to do. The conceptual background belongs in a linked term note or argument note. A procedure note should be scannable -- an operator in the middle of an incident should not have to read theory to find the next step.
- **Omitting prerequisites**: Starting a procedure with "Step 1: Run the query" without specifying which system, what credentials, what data must be available, or what prior steps must be completed. Missing prerequisites cause procedures to fail silently when used by someone other than the author.
- **Unnumbered or unordered steps**: Using bullet points for steps that must be performed in sequence. Bullets imply "do these in any order"; numbered steps communicate "do these in this order." Procedural notes must use numbered steps to communicate ordering.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: Parent term -- procedure is a vault extension to Sascha's taxonomy, adding knowing-how to the knowing-that building blocks
- **[Knowledge Building Blocks -- Hypothesis](term_knowledge_building_blocks_hypothesis.md)**: Sibling block -- hypotheses propose what to test; procedures specify how to test it
- **[Knowledge Building Blocks -- Empirical Observation](term_knowledge_building_blocks_empirical_observation.md)**: Sibling block -- procedures produce observations; observations motivate new procedures
- **[Knowledge Building Blocks -- Navigation](term_knowledge_building_blocks_navigation.md)**: Sibling block -- navigation notes organize access to procedures and other blocks
- **[Prescriptive Knowledge](term_prescriptive_knowledge.md)**: The broader epistemological category that procedures belong to -- knowledge of how to do things
- **[SOP](term_sop.md)**: Standard Operating Procedure -- a common instantiation of the procedure building block in operational contexts
- **[Heuristic](term_heuristic.md)**: Sascha's original building block for rules of thumb; procedures differ by being explicit, ordered, and complete rather than approximate

## References

### Vault Sources

- [entry_ari_sop_list.md](../../0_entry_points/entry_ari_sop_list.md) -- index of ARI SOP procedure notes in the vault
- [entry_how_to_guides.md](../../0_entry_points/entry_how_to_guides.md) -- index of how-to procedure notes

### External Sources

- Ryle, G. (1949). *The Concept of Mind*. Hutchinson. -- foundational argument for the knowing-how / knowing-that distinction.
- Anderson, J.R. (1983). *The Architecture of Cognition*. Harvard University Press. -- ACT* theory of procedural learning and memory.
- Sascha (2025). "The Complete Guide to Atomic Note-Taking." zettelkasten.de -- the expanded taxonomy that this vault extension builds upon.
