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
| `model` | How is it structured? | Structuring (relational) | Knowledge | Architecture, Components, Relationships, References | `resources/term_dictionary/` |
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

## Reading the layers as a workflow

The four layers form a knowledge-production cycle a vault embodies over time:

```
Knowledge layer  : empirical_observation → concept → model
Reasoning layer  : (model) → hypothesis → argument → counter_argument
Action layer     : (model) → procedure → (back to empirical_observation)
Meta layer       : navigation indexes the other three
```

A *useful* vault grows along this cycle. A vault dominated by `concept` notes is a glossary; one dominated by `procedure` notes is a runbook; one with all four layers in balance is a Tessellum.

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
