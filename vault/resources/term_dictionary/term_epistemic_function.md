---
tags:
  - resource
  - terminology
  - knowledge_management
  - epistemology
  - building_blocks
  - tessellum_core
keywords:
  - epistemic function
  - knowledge function
  - Building Block role
  - epistemic role
  - prescriptive ontology
  - reasoning step
topics:
  - Epistemology
  - Knowledge Management
  - Ontology
language: markdown
date of note: 2026-05-09
status: active
building_block: concept
note_second_category: term
---

# Term: Epistemic Function

## Definition

An **epistemic function** is the *role* a typed atomic note plays in the knowledge-construction cycle — what it *does* with respect to other notes. Every [Building Block](term_building_block.md) type in Tessellum has one defining epistemic function, and the 10 directed edges of the BB ontology name *transitions between functions* — the reasoning steps that produce one function's output as the next function's input.

Epistemic function is the answer to: *"What is this note for?"* Not topically (which the title and tags answer) and not structurally (which `building_block:` answers), but *epistemically* — what reasoning act does it perform?

## The Eight Functions

Each Building Block type has exactly one defining epistemic function:

| BB type | Epistemic function | What this note *does* |
|---|---|---|
| `empirical_observation` | **Testing** | Records evidence — what was measured, what happened |
| `concept` | **Naming** | Defines a thing — gives it a label and boundaries |
| `model` | **Structuring** | Formalizes relationships between named things |
| `hypothesis` | **Predicting** | Makes a falsifiable claim about what will happen |
| `argument` | **Claiming** | Asserts a position with reason and evidence |
| `counter_argument` | **Refuting** | Challenges a claim's premise, warrant, or evidence |
| `procedure` | **Doing** | Codifies how to act — operational sequence |
| `navigation` | **Indexing** | Routes readers to other notes |

These eight functions are not arbitrary. They form the **closed set of reasoning moves** that knowledge work decomposes into. Every act of building knowledge is one of: name something, observe something, structure named things, predict from structure, test the prediction, challenge the test, codify the result into action, or route others to all of the above.

## Why Epistemic Function Matters

Most note-taking systems treat all notes as *opaque* — markdown is markdown. The system has no idea whether a note is a definition, an experiment result, an argument, or a TODO. This means:

1. **The system cannot check completeness** — a hypothesis without falsifiability criteria is broken; a counter-argument without a target is decorative. But the system can't tell.
2. **The system cannot route reasoning** — given an observation, what should come next? A naming step. Given a hypothesis, what should follow? A test. The system can only prompt these if it knows the function.
3. **The system cannot diagnose vault health** — "this vault has many observations but few concepts" is a *naming gap*; "many models but few hypotheses" is a *prediction gap*. The diagnosis requires function-awareness.
4. **The system cannot retrieve by epistemic function** — "show me all the unresolved counter-arguments" is unanswerable in an untyped system; trivial in a function-typed one.

Naming the epistemic function in the YAML frontmatter (via `building_block:`) gives the system a handle on what each note *does*, which unlocks all four capabilities.

## Function vs Type vs Topic

These three are easily confused:

| Layer | Question it answers | Example value |
|---|---|---|
| **Topic** (tags / title) | What is the note *about*? | "PageRank" |
| **Type** (building_block) | What *kind* of note is it? | `concept` |
| **Function** (epistemic role) | What does it *do*? | Naming (defines PageRank as a labeled thing) |

Topic and type are both *attributes* of the note. Function is what those attributes *imply* about the note's role in reasoning. The same topic can appear in notes with different types, and therefore different functions:

- "PageRank" as a `concept` note → function is **naming** (defining what PageRank is)
- "PageRank" as a `model` note → function is **structuring** (showing how PageRank relates to other graph metrics)
- "PageRank" as a `procedure` note → function is **doing** (the steps to compute PageRank in this vault)
- "PageRank vs HITS" as an `argument` note → function is **claiming** (asserting one is preferable)

The same topic, three different functions. The function tells the system *what reasoning step the note belongs to*.

## The Reasoning Cycle as a Function Graph

The 10 directed edges of the [Building Block ontology](term_building_block.md) are *transitions between functions* — the reasoning steps that close the cycle:

```
Testing → (Naming) → Structuring → (Predicting) → Predicting → (Testing) → Claiming
                                  ↘ (Codifying)
                                    Doing → (Execution Data) → Testing
                                                                   │
                                              Refuting ← (Challenging) ← Claiming
                                              ↓ (Motivates new)
                                              Testing (cycle closes)
```

Read this as: an observation (Testing function) gets a name (Naming function transition); the named thing gets structured into a model (Structuring); the model is used to predict (Predicting); the prediction is tested (Testing again — cycle reaches first inflection); the test produces a claim (Claiming); the claim is challenged (Refuting); the challenge motivates new observation (Testing — cycle closes).

This is a **prescriptive** cycle — given a note in any function, the cycle tells you what comes next. It's the dialectic engine that the [Dialectic Knowledge System](term_dialectic_knowledge_system.md) walks at runtime.

## Function-Driven Format

Each epistemic function determines the *required structural sections* of its Building Block type:

| Function | BB type | Required sections |
|---|---|---|
| Naming | `concept` | Definition, Examples, References |
| Testing | `empirical_observation` | Observation, Method, Result, References |
| Structuring | `model` | Architecture, Components, Relationships, References |
| Predicting | `hypothesis` | Hypothesis, Reasoning, Falsifiability, References |
| Claiming | `argument` | Claim, Reason, Evidence, References |
| Refuting | `counter_argument` | Counter-claim, Reason, Strength, References |
| Doing | `procedure` | Setup, Steps, Validation, References |
| Indexing | `navigation` | Purpose, Index, Related Entry Points |

Format conformance is what makes function-typed retrieval reliable. If every `argument` note has a `## Claim` section, the system can extract claims by structural query — without parsing prose.

## Function and the Four Epistemic Layers

The eight functions group into four *epistemic layers* by the **kind of failure** their notes are vulnerable to:

| Layer | Functions | Failure mode |
|---|---|---|
| **Knowledge** | Testing, Naming, Structuring | Factual error (the world isn't this way) |
| **Reasoning** | Predicting, Claiming, Refuting | Logical error (the inference doesn't follow) |
| **Action** | Doing | Operational error (the procedure fails or harms) |
| **Meta** | Indexing | Organizational error (readers can't find things) |

A note's function determines which kind of error it can suffer, and therefore which kind of validation matters most. An `empirical_observation` is checked against the world; an `argument` is checked against logic; a `procedure` is checked by execution; a `navigation` note is checked by user testing.

## Heritage

The notion of function-typed atomic units traces to several sources:

- **Aristotle's *ergon*** — every thing has a defining function (the *ergon* argument from *Nicomachean Ethics*); a thing is well-formed when it performs its function well
- **John Searle's speech act theory** (1969) — utterances perform classifiable functions (assertion, question, promise, command); meaning is partly constituted by function
- **Stephen Toulmin's argumentation framework** (1958) — arguments decompose into claim / data / warrant / backing / qualifier / rebuttal, each a typed *function* in the argument
- **Sascha Fast's Knowledge Building Blocks** (zettelkasten.de, 2011) — applied function-typing to atomic notes; the immediate predecessor to Tessellum's BB ontology
- **The Dialectic Knowledge System** (FZ 8 in the parent project) — formalizes the function graph as a runtime that updates warrants from observed disagreement

## Related

- [Term: Building Block](term_building_block.md) — the type system that names epistemic functions per atomic unit
- [Term: Dialectic Knowledge System](term_dialectic_knowledge_system.md) — the runtime that walks the function graph
- [Term: Zettelkasten](term_zettelkasten.md) — the broader method that hosts function-typed atomic notes
- [Term: Folgezettel](term_folgezettel.md) — trails that record argument descent (function transitions)
- [Term: CQRS](term_cqrs.md) — function-typed substrate (System P) ⊥ retrieval (System D)

## References

- Aristotle. *Nicomachean Ethics*, Book I (the *ergon* argument).
- Searle, J. R. (1969). *Speech Acts: An Essay in the Philosophy of Language*. Cambridge University Press.
- Toulmin, S. E. (1958). *The Uses of Argument*. Cambridge University Press.
- Fast, S. (2011–). [Knowledge Building Blocks: A Universal Method for Note-Taking](https://zettelkasten.de/posts/atomic-note-types/). zettelkasten.de.
- The Tessellum extension to 8 functions (adding Doing/Procedure and Indexing/Navigation) and the 10-edge function graph were derived in Folgezettel trail FZ 7g of the parent research project.
