---
tags:
  - resource
  - how_to
  - folgezettel
  - trail
  - knowledge_construction
keywords:
  - Folgezettel trail
  - argumentative descent
  - FZ ID assignment
  - extend a trail
  - branch a trail
  - DKS cycle FZ output
topics:
  - Folgezettel
  - Knowledge Construction
  - Vault Workflow
language: markdown
default of note: 2026-05-11
date of note: 2026-05-11
status: active
building_block: procedure
bb_schema_version: 1
---

# How To: Author a Folgezettel Trail

Folgezettel (FZ) trails are Tessellum's mechanism for *argumentative descent* — chains of notes where each child node *refines, defends, or attacks* its parent's claim. This guide walks through authoring the first root, extending it with descendants, branching at decision points, and using DKS cycles to grow trails machine-produced.

## What a trail is, in one paragraph

A FZ trail is a tree of notes where each node's `folgezettel:` field is a hierarchical ID (`1`, `1a`, `1a1`, `1a1b`, ...) and `folgezettel_parent:` points at the parent's FZ. The hierarchy *encodes the argumentative structure*: `1` is a root claim, `1a` refines it, `1b` is a sibling refinement, `1a1` refines `1a` further. Reading a trail breadth-first gives the conceptual map; reading depth-first gives the argumentative descent.

For the full theory, see [`term_folgezettel`](../term_dictionary/term_folgezettel.md).

## Step 1: Author the trail root

Pick the next unused top-level integer FZ:

```bash
tessellum fz next-root --vault vault
# → "4" (the next free top-level FZ)
```

Then capture an `argument`-typed note for the root claim:

```bash
tessellum capture argument my_new_trail_root --vault vault
# → vault/resources/analysis_thoughts/thought_my_new_trail_root.md
```

Edit the new note's frontmatter:

```yaml
folgezettel: "4"
folgezettel_parent: ""   # roots have no parent
argument_perspective: "conservative"  # optional; for multi-perspective DKS later
```

Write the root's `## Claim`, `## Reason`, `## Evidence` sections — the seed of the argumentative chain.

## Step 2: Extend the trail with a descendant

When you want to add a child node (a refinement, defense, or attack of the parent):

```bash
tessellum fz next-child --parent 4 --vault vault
# → "4a" (first child of 4)
```

Capture the child note:

```bash
tessellum capture argument my_refinement --vault vault
```

Set frontmatter:

```yaml
folgezettel: "4a"
folgezettel_parent: "4"
```

Body should *explicitly relate* to the parent — common framings:

- *Refinement*: "FZ 4's claim holds for the general case, but only conditionally for X. Here's why X matters: ..."
- *Defense*: "FZ 4's strongest objection is Y. This note shows Y doesn't apply because ..."
- *Sharpening*: "FZ 4 conflates two senses of Z. This note disambiguates ..."

The Reason / Evidence sections cite the parent's claim verbatim; the Counter section names known objections (which become candidate FZ 4a1 / 4a2 children later).

## Step 3: Branch at a decision point

When FZ 4's argument leaves a *choice* — e.g., "X could be approached via Y or Z" — each branch gets its own child:

- FZ 4a → "approach X via Y" (explores Y)
- FZ 4b → "approach X via Z" (explores Z)

Author both. Trails *branch* at decision points and *converge* via cross-references in `## Related Notes`. The hierarchy makes the branching structure machine-readable.

## Step 4: Counter your own claim

Strong trails *include* their own counter-arguments. After authoring FZ 4a, the natural next move is FZ 4a1 — a `counter_argument`-typed note attacking FZ 4a:

```bash
tessellum capture counter_argument against_my_refinement --vault vault
```

Frontmatter:

```yaml
folgezettel: "4a1"
folgezettel_parent: "4a"
building_block: counter_argument
```

The TESS-004 validator enforces a structural invariant: every `counter_argument` note must link to the attacked argument note via folgezettel hierarchy. Setting `folgezettel_parent: "4a"` satisfies this — the counter's FZ descends from the argument it attacks.

The counter must name **which Toulmin component is broken** in FZ 4a's argument:

- **premise** — the data field is wrong
- **warrant** — the inference rule from data to claim doesn't hold
- **counter-example** — there's a specific case where the claim fails
- **undercutting** — the warrant's *applicability* is contested

This is the same vocabulary DKS cycles use (per `step 5_counter_argument_capture` in [`skill_tessellum_dks_cycle`](../skills/skill_tessellum_dks_cycle.md)).

## Step 5: Update the per-trail entry point

Every trail has a per-trail entry point under `vault/0_entry_points/entry_<trail_name>_trail.md`. After authoring new FZ nodes, update the entry point's ASCII tree + FZ table:

```bash
tessellum fz tree --root 4 --vault vault
# → prints the tree of FZ 4 + all descendants
```

Copy that into the entry point's `## ASCII Tree` section + add the new node's row to the `## FZ Table`.

Per the memory rule (project-internal): always update the **child entry point first** (e.g., `entry_dialectic_trail.md`) before the parent `entry_folgezettel_trails.md` master index — the master aggregates from the child.

## Step 6 (optional): Let DKS grow the trail for you

Once you've manually authored a trail root + a few nodes, DKS cycles can take over. Each DKS cycle on an observation deposits a 6-node FZ subtree:

```
parent: <existing FZ>
└── cycle_root (empirical_observation)
    ├── cycle_root.a (argument, conservative)
    ├── cycle_root.b (argument, exploratory)
    │   └── cycle_root.b.a (counter_argument, when A and B disagree)
    │       └── cycle_root.b.a.a (model, the pattern discovered)
    │           └── cycle_root.b.a.a.a (procedure/concept, the revised warrant)
```

Run a cycle in `--mode extend` to grow an existing trail:

```bash
tessellum dks runs/observations.jsonl \
    --mode extend \
    --parent-fz 4a \
    --backend anthropic
# → deposits new FZ subtree under 4a
```

The cycle's `surviving_argument_fzs` property surfaces which arguments survived the dialectic (per Dung grounded labelling, v0.0.54+); those FZs are the candidates to extend in subsequent cycles.

For multi-perspective cycles (v0.0.54+):

```bash
tessellum dks runs/observations.jsonl \
    --perspectives conservative,exploratory,empirical \
    --backend anthropic
# → 3 argument nodes per observation; pairwise contradicts; Dung labelling
```

See [`thought_dks_design_synthesis`](../analysis_thoughts/thought_dks_design_synthesis.md) (FZ 2a) for the full 7-component pattern.

## Trail anti-patterns

| Anti-pattern | Fix |
|---|---|
| Skipping the counter-argument step | Every claim should have at least one explicit `counter_argument` child node; trails without counters become brittle |
| FZ IDs reused across trails | Each trail root's integer is unique; descendants extend the parent's prefix. `tessellum fz next-root` enforces this. |
| `folgezettel_parent:` missing on non-roots | TESS-001 ERROR. Fix by setting the parent FZ or marking the note as a root (no parent). |
| Trail tree only goes one direction (no branching) | A trail with no siblings is a single-path argument — sound but rigid. Branch on choice points to capture alternatives. |
| Per-trail entry point not updated when new nodes land | Future readers can't navigate the trail. The entry point is the canonical map. |

## Run the FZ validator

```bash
tessellum fz validate --vault vault
# → checks every FZ in the vault for:
#     - parent existence (TESS-001)
#     - hierarchy consistency (parent FZ is the prefix of child FZ)
#     - no duplicates
```

The CLI returns exit code 1 if any errors exist.

## Related Notes

- [`term_folgezettel`](../term_dictionary/term_folgezettel.md) — the FZ mechanism in full
- [`thought_dks_design_synthesis`](../analysis_thoughts/thought_dks_design_synthesis.md) — FZ 2a, the DKS cycle that produces FZ subtrees machine-readably
- [`thought_dks_fz_integration`](../analysis_thoughts/thought_dks_fz_integration.md) — FZ 2a1, the spatial sharpening (DKS × FZ as one mechanism)
- [`howto_first_vault`](howto_first_vault.md) — getting-started prerequisite
- [`howto_note_format`](howto_note_format.md) — frontmatter spec including FZ fields

## See Also

- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail index
- [`skill_tessellum_traverse_folgezettel`](../skills/skill_tessellum_traverse_folgezettel.md) — agent-invocable trail walker
- [`skill_tessellum_append_to_trail`](../skills/skill_tessellum_append_to_trail.md) — agent-invocable trail extender
