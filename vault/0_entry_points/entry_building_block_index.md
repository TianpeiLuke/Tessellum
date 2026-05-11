---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - building_block
  - ontology
keywords:
  - building block picker
  - epistemic function
  - epistemic edges
  - typed atomic note ontology
  - BB classification
topics:
  - Building Block Ontology
  - Navigation
  - Note Classification
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Building Block Index

Pick the right `building_block:` for a new note. Each row is one of the 8 types, with the question it answers, its epistemic function, where notes of that type live, and the required H2 sections it must contain.

For the full *why* of each type — origin, examples, when to reach for it — read [`term_building_block`](../resources/term_dictionary/term_building_block.md). This index is the scannable picker; the term note is the depth.

## The 8 Building Block types

| BB type | Question it answers | Epistemic function | Layer | Required sections | Default directory |
|---|---|---|---|---|---|
| `empirical_observation` | What happened? | Testing (observe → record) | Knowledge | Observation, Method, Result, References | `resources/analysis_thoughts/` |
| `concept` | What is it called? | Naming (boundary-drawing) | Knowledge | Definition, Examples, References | `resources/term_dictionary/` |
| `model` | How is it structured? | Structuring (relational) | Knowledge | Architecture, Components, Relationships, References | `areas/` (with sub-categories like `areas/code_repos/`, `areas/tools/`, `areas/teams/`) |
| `hypothesis` | What will happen next? | Predicting (forward-looking) | Reasoning | Hypothesis, Reasoning, Falsifiability, References | `resources/analysis_thoughts/` |
| `argument` | Is the prediction true? | Claiming (justified position) | Reasoning | Claim, Reason, Evidence, References | `resources/analysis_thoughts/` |
| `counter_argument` | What are the flaws? | Refuting (challenging) | Reasoning | Counter-claim, Reason, Strength, References | `resources/analysis_thoughts/` |
| `procedure` | How do we act on this? | Doing (operationalizing) | Action | Setup, Steps, Validation, References | `resources/how_to/` or `resources/skills/` |
| `navigation` | Where does this live? | Indexing (routing) | Meta | Purpose, Index, Related Entry Points | `0_entry_points/` |

**Reading the layers**: a Tessellum vault grows in layers — *Knowledge* (observation → concept → model) feeds *Reasoning* (hypothesis → argument → counter-argument) feeds *Action* (procedure), and *Meta* (navigation) routes between them. The full cycle is encoded in the 10 epistemic edges below.

## The 10 epistemic edges (the DKS dialectic graph)

Each edge says *one type produces the next*. Together they form the closed-loop dialectic that the Dialectic Knowledge System ([`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md)) operationalizes.

| # | Source | → | Target | Label | What the edge means |
|--:|---|---|---|---|---|
| 1 | `empirical_observation` | → | `concept` | Naming & Defining | Observed regularities get named |
| 2 | `concept` | → | `model` | Structuring | Concepts compose into relational structures |
| 3 | `model` | → | `hypothesis` | Predicting | Structures generate testable predictions |
| 4 | `model` | → | `procedure` | Codifying | Structures generate actionable workflows |
| 5 | `hypothesis` | → | `argument` | Testing & Evidence | Predictions get tested; evidence supports a claim |
| 6 | `argument` | → | `counter_argument` | Challenging | Every claim invites refutation |
| 7 | `counter_argument` | → | `empirical_observation` | Motivates new | Refuted claims drive new observations |
| 8 | `procedure` | → | `empirical_observation` | Execution Data | Running a procedure produces new observations |
| 9 | `navigation` | → | `empirical_observation` | Indexes | Index notes route readers to observations |
| 10 | `navigation` | → | `concept` | Indexes | Index notes route readers to concepts |

The cycle: observation → concept → model → (hypothesis, procedure) → (argument, observation) → counter → observation. **Cycles close** — refuting an argument doesn't end the inquiry; it triggers new observations. This is why "dialectic" rather than "logic": the system updates rather than concludes.

## How to use this index

### "Which BB type should my note be?"

Ask the question at the top of each row:

- *What is it called?* → `concept` (a term-dictionary note)
- *How is this structured?* → `model` (still a term-dictionary note, but with architecture)
- *What happened?* → `empirical_observation` (an analysis-thoughts note)
- *I predict X will happen if Y* → `hypothesis`
- *I claim X because Y, evidenced by Z* → `argument`
- *X is wrong because Y* → `counter_argument`
- *Here are the steps to do X* → `procedure`
- *Where is everything?* → `navigation`

### "Which sections do I need?"

The "Required sections" column lists the H2 sections each BB must have. Templates under [`resources/templates/`](../resources/templates/) bake these in — `template_concept.md` starts with `## Definition`, `## Examples`, etc. Filling a template gives you a valid note by construction.

### "Where does my note land?"

The "Default directory" column matches the capture registry. `tessellum capture <flavor> <slug>` writes to the right place automatically. If you author manually, place the file under the listed directory.

**Convention: `term_dictionary/` is concept-only.** Notes in `resources/term_dictionary/` should always be `building_block: concept` (they answer *"what is it called?"*). Structural notes — those answering *"how is it structured?"* — are `model`-typed and live in `areas/` with appropriate sub-categories (`areas/code_repos/` for repo architecture, `areas/tools/` for algorithms, `areas/teams/` for team structure, etc.). Two legacy `term_dictionary/` files (`term_format_spec.md`, `term_pixie_random_walk.md`) currently violate this convention; relocation is pending.

**The directories above are defaults, not constraints.** `tessellum capture <flavor> <slug>` writes to the registry's default location, but agents/callers know the specific note's sub-category better than the registry can. Pass `--destination <subdir>` and `--prefix <name_>` to land a note where it belongs — e.g., `tessellum capture model my_algo --destination areas/tools --prefix tool_` lands a model-typed algorithm note at `areas/tools/tool_my_algo.md`. The registry default is a sensible starting point when the agent has no better information.

## Reading the layers as a workflow

The four layers form a knowledge-production cycle a vault embodies over time:

```
Knowledge layer  : empirical_observation → concept → model
Reasoning layer  : (model) → hypothesis → argument → counter_argument
Action layer     : (model) → procedure → (back to empirical_observation)
Meta layer       : navigation indexes the other three
```

A *useful* vault grows along this cycle. A vault dominated by `concept` notes is a glossary; one dominated by `procedure` notes is a runbook; one with all four layers in balance is a Tessellum.

## Canonical exemplars — one per BB type

For each Building Block, this table points at a real, well-formed note in this seed vault that exemplifies the type. Read the exemplar to see what its question — "What happened?" / "What is it called?" / etc. — actually looks like *answered* in concrete prose. The exemplars are real vault content, not synthetic teaching examples: they prove the BB pattern survives substantive material.

| BB type | Question it answers | Canonical exemplar | What you'll learn from it |
|---|---|---|---|
| `empirical_observation` | **What happened?** | [`paper_khattab2023dspy_exp_result`](../resources/papers/paper_khattab2023dspy_exp_result.md) | A factual, past-tense record of an experiment's measured outcomes — no interpretation, just data. The DKS-cycle `q₀` shape: what gets fed into step 1. |
| `concept` | **What is it called?** | [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) | A named entity (DKS) defined with full Toulmin-style backing: heritage, definition, when to invoke. The reference shape every other note links *into*. |
| `model` | **How is it structured?** | [`repo_tessellum`](../areas/code_repos/repo_tessellum.md) | A repository decomposed into 8 first-class components + their inter-component flows + the build system that ships them. The shape an `argument` builds *on top of*. Lives in `areas/` because `model` notes describe ongoing structured systems, not named entities (those go to `concept` in `term_dictionary/`). |
| `hypothesis` | **What will happen next?** | [`lit_khattab2023dspy`](../resources/papers/lit_khattab2023dspy.md) | A falsifiable forward-looking claim with stated test conditions. Drives an `argument` once evidence accumulates; retires to `archived` when settled. |
| `argument` | **Is the prediction true?** | [`thought_dks_design_synthesis`](../resources/analysis_thoughts/thought_dks_design_synthesis.md) | A reasoned position with full Toulmin structure: claim + data + warrant + qualifier + rebuttal. The synthesis shape that anchors an FZ trail node. |
| `counter_argument` | **What are the flaws?** | [`counter_two_systems_not_three_ontology_and_dks_are_one`](../resources/analysis_thoughts/counter_two_systems_not_three_ontology_and_dks_are_one.md) | A targeted attack on a specific argument's warrant or premise. Names *which Toulmin component is broken* and proposes a tightening. Step 5 output shape. |
| `procedure` | **How do we act on this?** | [`skill_tessellum_dks_cycle`](../resources/skills/skill_tessellum_dks_cycle.md) | An operational rule expressed as agent-invocable canonical: setup, step-by-step, error handling, constraints. The "do X to get Y" shape. |
| `navigation` | **Where does this live?** | [`entry_dialectic_trail`](entry_dialectic_trail.md) | A typed index over a coherent slice of the vault (here, the FZ 2 dialectic trail). Routes readers; doesn't argue. The meta-layer shape. |

Each exemplar pairs with the corresponding row in the "8 Building Block types" table above. To author your own note of a type, start by reading its exemplar — it shows the H2 sections, voice, and density that work for that type. Then copy the template from `vault/resources/templates/` (or run `tessellum capture <flavor> <slug>` which does it for you).

## Related Entry Points

- [`entry_master_toc`](entry_master_toc.md) — the vault's navigation root
- [`entry_acronym_glossary`](entry_acronym_glossary.md) — master index of the 5 universal acronym glossaries

## Related Terms

- [`term_building_block`](../resources/term_dictionary/term_building_block.md) — full depth on the 8-type ontology
- [`term_epistemic_function`](../resources/term_dictionary/term_epistemic_function.md) — what each function (naming / structuring / predicting / ...) actually does
- [`term_knowledge_building_blocks`](../resources/term_dictionary/term_knowledge_building_blocks.md) — the historical predecessor (Sascha Fast)
- [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) — the cycle the 10 edges close
- [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) — the format contract `building_block:` participates in

---

**Last Updated**: 2026-05-10
**Status**: Active — derived from `tessellum.format.building_blocks.BB_SPECS` + `EPISTEMIC_EDGES`
