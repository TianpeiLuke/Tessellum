---
tags:
  - resource
  - analysis
  - argument
  - cqrs
  - architecture
  - synthesis
keywords:
  - CQRS essence
  - Tessellum architecture thesis
  - System P System D
  - declaration vs computation
  - one boundary
  - typed knowledge
topics:
  - System Architecture
  - CQRS
  - Tessellum Core Thesis
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "1a1a"
folgezettel_parent: "1a1"
---

# The Essence of CQRS for Tessellum — One Boundary, Two Disciplines

## Thesis

After the four-step descent from typed BB graph to two-system synthesis, the CQRS shape compresses to a single load-bearing claim:

> **A typed-knowledge slipbox should split its read path and its write path across one boundary, the boundary between declaration and computation, and share exactly one substrate between them.**

Everything else about Tessellum's architecture — what ships in the vault, where the indexer writes, what Composer does, how runtime traces are filed, what MCP would plug into if added later — falls out of that claim. This note is the distilled form for users who don't need the history; the history lives in [`thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md). The synthesis it descends from is [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md).

## The boundary

Tessellum has exactly one architectural seam:

```
            DECLARATION                                COMPUTATION
                │                                          │
                ▼                                          ▼
    ┌──────────────────────┐                ┌─────────────────────────┐
    │   System P            │                │   System D               │
    │   (Prescriptive)      │                │   (Descriptive)          │
    │                       │                │                          │
    │   Authors write       │                │   Indexer + retrieval    │
    │   typed atomic notes  │                │   read the vault         │
    │   per the format spec │                │   and produce ranked     │
    │   + the BB ontology.  │                │   answers to queries.    │
    │                       │                │                          │
    │   Composer is here    │                │   tessellum search,      │
    │   (it writes notes).  │                │   tessellum filter,      │
    │                       │                │   tessellum composer run │
    │                       │                │   (when reading) are     │
    │                       │                │   here.                  │
    └─────────────┬─────────┘                └────────────┬─────────────┘
                  │                                       │
                  │       ONE SHARED SUBSTRATE            │
                  │       ──────────────────────          │
                  │                                       │
                  └──────────────► vault/  ◄──────────────┘
                                   (markdown + YAML)
                                   P writes; D reads.
```

The boundary is between **what you assert** (System P) and **what you can infer from what's asserted** (System D). One side is correct or incorrect by the format spec and the BB ontology. The other side is good or bad by retrieval-quality metrics.

## Why this matters in practice

The two-system split gives Tessellum three useful properties no single-system design has:

### 1. The two disciplines can be evaluated separately

| Side | How you know it's working | How you know it's broken |
|---|---|---|
| System P | `tessellum format check .` passes; every note's `building_block:` is meaningful for the claim it makes; FZ trails resolve | Schema rot, BB-types proliferating ad-hoc, untyped fields creeping in |
| System D | Top-K retrieval matches your intent; hybrid RRF lift over BM25 is measurable; agents using the index produce useful answers | Hit-quality regression, embedding drift, hybrid blending broken |

A System P bug doesn't masquerade as a retrieval bug, and vice versa.

### 2. The two sides can change independently

| Change | Affects System P? | Affects System D? |
|---|---|---|
| New BB type | ✓ — extend the ontology | — (D reads whatever P writes) |
| New retrieval strategy (e.g., add re-ranker) | — | ✓ — D-internal |
| New skill canonical | ✓ — P writes notes; the skill is part of P | — |
| Re-index with a different embedding model | — | ✓ — D rebuilds |
| DKS dialectic protocol revision | ✓ — DKS is internal to P | — |
| Switch SQLite → DuckDB for the index | — | ✓ — D-internal |

Changes that look like they should cascade across systems mostly don't, because the shared substrate (the vault) hides the implementation details on each side from the other.

### 3. One substrate prevents drift

Most production systems with separate read and write paths end up with **two substrates** that have to be kept in sync — a write database and a read database, with a replication lag and a reconciliation problem. Tessellum has one substrate (the vault) and lets the indexer rebuild whenever the vault changes. The reconciliation problem reduces to "did you run `tessellum index build`?"

## The rules that fall out

Once the boundary is the architectural commitment, downstream rules follow:

1. **System D never mutates the vault.** Retrieval reads, ranks, returns. No re-writing on retrieval. If a query reveals a missing note, that's an authoring task (System P), not a retrieval task.
2. **System P never queries the index for *what should be true*.** P writes truths by declaration (typed atomic notes); it does not poll D for guidance on what to write. (P may invoke D for read-only context — but the *decision* is P's.)
3. **The substrate is single-rooted at `vault/`.** Everything that's part of the knowledge state lives under `vault/`. Build artifacts (`data/`) and runtime traces (`runs/`) are *outputs*, not substrate — they're gitignored, regenerable, and live outside `vault/`.
4. **Composer is a System P runtime.** Composer writes notes. It may read the index (System D) for context, but its job is to produce vault content per a typed contract. Composer's `runs/composer/` traces document the bridge between P (what was authored) and the agent that did the authoring; they belong outside both systems.
5. **MCP, when added, plugs into System D.** An MCP server exposing Tessellum to other agents will expose *queries*, not *writes*. Writes go through `tessellum capture` + skills + Composer, all of which are System P. (This is a v0.2+ design constraint, recorded here so the decision doesn't have to be re-litigated.)

## What CQRS is *not*

It is worth naming what this is not, because conventional CQRS has connotations that don't apply here:

- **Not a database pattern.** Conventional CQRS splits the *write store* from the *read store* (separate SQL databases, often with event sourcing in between). Tessellum's split is at the *knowledge layer*: same pattern, different substrate. The vault is one filesystem of markdown files.
- **Not eventual consistency.** There is no consistency lag — the index is a deterministic function of the vault. `tessellum index build` rebuilds it from scratch in seconds.
- **Not microservices.** P and D are not separate processes. They are separate *disciplines* in the same codebase. You can use System D without ever touching System P (read-only consumer of someone else's vault), and you can use System P without System D (author + validate without ever indexing). They compose at the substrate; they don't require IPC.
- **Not a replacement for the BB ontology.** The BB ontology is *internal to System P* — it's the vocabulary by which System P writes typed atomic notes. CQRS is the architectural commitment that *uses* the typed substrate; the typed substrate exists prior to CQRS.

## How to check yourself

When making any architectural decision in Tessellum, ask one question:

> Which side of the declaration / computation boundary does this belong on?

If the answer is "both" or "neither" or "a new third side," **stop**. Either the proposed change is two changes (one per side, possibly), or it's recreating the three-regime confusion the descent already worked through and rejected. Read [`thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md) for the explicit argument.

The boundary is the architectural commitment. Defending it is the architectural discipline.

## Related Notes

- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the parent synthesis this note distills
- [`thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md) — FZ 1a — the four-step descent that arrived at the synthesis
- [`thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — FZ 1 — the substrate System P is defined over
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — the canonical term definition
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS, which the descent revealed to be internal to System P
- [`term_format_spec`](../term_dictionary/term_format_spec.md) — the regularization System P enforces

## See Also

- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — the FZ trail map; this note is the leaf of the Architecture trail
- [`entry_master_toc`](../../0_entry_points/entry_master_toc.md) — vault navigation root

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 1a1a (leaf), Architecture trail
