---
tags:
  - entry_point
  - index
  - navigation
  - folgezettel
  - trail_map
keywords:
  - folgezettel trails
  - FZ trail map
  - argument descent
  - master trail index
  - trail navigation
topics:
  - Navigation
  - Folgezettel
  - Trail Map
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Folgezettel Trail Map — Master Index

## Purpose

This is the **master index** of all Folgezettel trails in the vault. Each trail is a sequence of typed atomic notes whose `folgezettel:` IDs encode *how thinking developed* — argument → counter → response → synthesis — descended alphanumerically (`1 → 1a → 1a1 → 1a1a`). Each trail has its own per-trail entry point that holds the trail's ASCII tree, FZ table, dialectic summary, and reading order. **This page links to those per-trail entry points; it does not duplicate their content.**

For the *what* of Folgezettel as a mechanism, see [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md). For *how to grow* a trail, see the bottom of this page.

## Trails shipped in the seed vault

| Trail # | Root note | Per-trail entry point | Nodes | Subject |
|--:|---|---|--:|---|
| **1** | [`thought_building_block_ontology_relationships`](../resources/analysis_thoughts/thought_building_block_ontology_relationships.md) | [Architecture Trail](entry_architecture_trail.md) | 8 | From the typed BB graph to two-system CQRS + R-Cross rules + gap audit + graph-formalisation (1b) + BB-internal-transitions counter (1c) |
| **2** | [`thought_dks_evolution`](../resources/analysis_thoughts/thought_dks_evolution.md) | [Dialectic Trail](entry_dialectic_trail.md) | 6 | How DKS was reasoned into shape: 7-component closed loop + DKS × FZ unification + DKS-as-FSM-on-BB-graph + runtime integration + transition-model adaptation (2c) |
| **3** | [`thought_retrieval_evolution`](../resources/analysis_thoughts/thought_retrieval_evolution.md) | [Retrieval Trail](entry_retrieval_trail.md) | 2 | How retrieval was tested into shape: 14-strategy bake-off → unified engine + hybrid RRF + best-first BFS |

**3 trails, 16 nodes total.** Each trail's per-trail entry point is the place to start when reading the trail; this master page exists only to tell you which trails exist and where to find them.

## Why per-trail entry points

A trail's argumentative shape — what was tried, what was rejected, why the synthesis survived — is load-bearing context that doesn't fit in a single sentence. Putting that context on the master page (this page) would crowd the index as trails accumulate. So the convention is:

- **Master page** (this file) — one row per trail, just enough to tell you where to go.
- **Per-trail entry point** — the trail's ASCII tree, FZ table, dialectic summary, reading order, related trails, and "what this trail rejects" carve-outs.

When a new trail joins the vault, it gets its own `entry_<trail_name>_trail.md` and a row here.

## How to grow a new trail

Three steps to start a new trail (call it *Trail N*):

### 1. Pick a trail number

Use the next free integer at the top level (`1`, `2`, `3`, ...). The integer carries no ordering — trails are independent argumentative chains, not phases of one larger argument.

### 2. Author the trail-root note

The root sits at `folgezettel: "N"` with `folgezettel_parent: ""` (empty string — the both-or-neither rule requires the field to be *present*; the value `""` marks "this is the trail root"). Place the file under `vault/resources/analysis_thoughts/` (or wherever its BB type belongs — most trail nodes are `argument` or `counter_argument`, which capture under `analysis_thoughts/`).

### 3. Author the per-trail entry point

Create `vault/0_entry_points/entry_<trail_name>_trail.md` with `building_block: navigation`. Use the existing two entry points ([Architecture](entry_architecture_trail.md), [Dialectic](entry_dialectic_trail.md)) as templates. The entry point must include:

- ASCII tree of the trail (visualising the descent)
- FZ table (one row per node: FZ ID, note link, BB type, role)
- Summary of the dialectic progress (what each step rejected and what the final synthesis claims)
- Reading order (top-down for first read, leaf-up for re-reads)
- "What this trail rejects" carve-outs (so a reader understands which alternatives were considered and why they failed)

### 4. Add a row here

Append a row to the "Trails shipped in the seed vault" table above:

```markdown
| **N** | [`thought_<root>`](../resources/analysis_thoughts/thought_<root>.md) | [<Name> Trail](entry_<name>_trail.md) | <nodes> | <one-line subject> |
```

### 5. Grow downward by adding children

To add a child to an existing trail node (FZ ID `Nx`):

1. Append the next suffix:
   - Letter → branch (`Nx` → `Nxa`, `Nxb`, `Nxc`, ...)
   - Number → continue the chain (`Nx` → `Nx1`, `Nx2`, ...)
2. Set the new note's frontmatter:
   ```yaml
   folgezettel: "Nxa"
   folgezettel_parent: "Nx"
   ```
   Both fields must be present (`TESS-001` / `TESS-002` enforce the both-or-neither rule). Empty `folgezettel_parent: ""` is reserved for trail roots.
3. Update the per-trail entry point — add a row in the FZ table; extend the ASCII tree.

The validator and indexer pick up the new note automatically; no other configuration changes.

## Why ship FZ trails in the seed?

A new Tessellum user reads [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) (the mechanism) and [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) (the rules), but until they see a real trail in action, the convention is abstract. The two shipped trails are worked examples: every FZ ID is real, every parent-child pair is valid, every link resolves, and the resulting chains record the actual design history of Tessellum's two most novel architectural commitments (CQRS and DKS).

When you grow your first trail, copy the shape: linear or branching descent, a root with `folgezettel_parent: ""`, a per-trail entry point that summarises the dialectic progress, and a row in this master index.

## Related Entry Points

- [`entry_master_toc`](entry_master_toc.md) — vault navigation root
- [`entry_architecture_trail`](entry_architecture_trail.md) — Trail 1 (Architecture / CQRS)
- [`entry_dialectic_trail`](entry_dialectic_trail.md) — Trail 2 (Dialectic / DKS)
- [`entry_retrieval_trail`](entry_retrieval_trail.md) — Trail 3 (Retrieval / System D)
- [`entry_building_block_index`](entry_building_block_index.md) — BB picker matrix (each trail note declares a `building_block:`)
- [`entry_acronym_glossary`](entry_acronym_glossary.md) — acronym glossaries master index

## Related Terms

- [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) — the trail mechanism this map indexes
- [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) — the `folgezettel:` / `folgezettel_parent:` field rules

---

**Last Updated**: 2026-05-10
**Status**: Active — 3 trails shipped (Architecture, Dialectic, Retrieval), 16 nodes total (FZ 1c + FZ 2c paired addition: BB-internal-transitions evidence and DKS transition-model adaptation strategy, both 2026-05-10)
